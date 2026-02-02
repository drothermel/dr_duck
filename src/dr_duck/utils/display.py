from __future__ import annotations

import inspect
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar, TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    import marimo as mo
    from marimo._plugins.ui._core.ui_element import UIElement

TModel = TypeVar("TModel", bound=BaseModel)

__all__ = [
    "add_marimo_display",
    "defining_path",
    "relative_to_safe",
    "render_model",
    "resolve_repo_root",
]

_marimo_available = False
try:
    import marimo as mo
    from marimo._plugins.ui._core.ui_element import UIElement
    _marimo_available = True
except ImportError:
    mo = None
    UIElement = None


def defining_path(obj: Any) -> Path | None:
    if src := inspect.getsourcefile(obj) or inspect.getfile(obj):
        return Path(src).resolve()
    mod_name = getattr(obj, "__module__", None)
    mod = sys.modules.get(mod_name) if mod_name else None
    mod_file = getattr(mod, "__file__", None) if mod else None
    return Path(mod_file).resolve() if mod_file else None


def resolve_repo_root(model: BaseModel) -> Path:
    if hasattr(model, "repo_root"):
        if repo_root := model.repo_root:
            return Path(repo_root)
    elif (
        hasattr(model, "paths")
        and (model.paths and hasattr(model.paths, "repo_root"))
        and (repo_root := model.paths.repo_root)
    ):
        return Path(repo_root)
    return Path(__file__).resolve().parent.parent.parent


def relative_to_safe(path: Path, base: Path) -> Path:
    try:
        return path.relative_to(base)
    except ValueError:
        return path


def render_model(
    model: BaseModel, class_path: Path | str | None
) -> UIElement | Any:
    assert _marimo_available, "marimo is required for render_model. Install with: pip install dr-duck[marimo]"
    class_path = class_path or "Unknown"
    rel_path = (
        class_path
        if isinstance(class_path, str)
        else relative_to_safe(class_path, resolve_repo_root(model))
    )
    rel_path_str = f"<small>`{rel_path}`</small>"
    return mo.vstack(
        [
            mo.md(f"**{model.__class__.__name__}** | {rel_path_str}"),
            model.model_dump(),
        ]
    )


def add_marimo_display() -> Callable[[type[TModel]], type[TModel]]:
    def decorator(cls: type[TModel]) -> type[TModel]:
        if not _marimo_available:
            return cls

        class_path = defining_path(cls)

        def _display_(self: BaseModel) -> Any:
            return render_model(self, class_path)

        cls._display_ = _display_
        return cls

    return decorator
