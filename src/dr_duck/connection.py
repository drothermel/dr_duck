from __future__ import annotations

import os
from pathlib import Path

import duckdb
from dotenv import load_dotenv

__all__ = ["open_motherduck_connection"]


def open_motherduck_connection(
    *,
    env_file: Path | str | None = None,
    motherduck_token: str | None = None,
    hf_token: str | None = None,
) -> duckdb.DuckDBPyConnection:
    if env_file:
        load_dotenv(env_file)

    md_token = motherduck_token or os.environ.get("MOTHERDUCK_TOKEN")
    assert md_token, "MOTHERDUCK_TOKEN not found in environment or .env file"

    conn = duckdb.connect(f"md:?motherduck_token={md_token}")

    hf = hf_token or os.environ.get("HF_TOKEN")
    if hf:
        conn.execute(
            f"""
            CREATE SECRET IF NOT EXISTS hf_token (
                TYPE HUGGINGFACE,
                TOKEN '{hf}'
            );
            """
        )

    return conn
