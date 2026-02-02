# dr-duck

DuckDB and MotherDuck utilities for data ingestion and HuggingFace integration.

## Installation

```bash
pip install dr-duck
```

Or with uv:
```bash
uv add dr-duck
```

For marimo notebook support:
```bash
pip install dr-duck[marimo]
```

## Features

### MotherDuck Connection

```python
from dr_duck.motherduck import open_motherduck_connection

conn = open_motherduck_connection()
```

### HuggingFace Integration

```python
from dr_duck.hf import (
    HFLocation,
    cached_download_tables_from_hf,
    query_hf_with_duckdb,
    upload_file_to_hf,
)

# Define a HuggingFace location
loc = HFLocation(repo_id="username/dataset", path="data.parquet")

# Download and cache parquet files
tables = cached_download_tables_from_hf(loc)

# Query HuggingFace data directly with DuckDB
result = query_hf_with_duckdb(conn, "SELECT * FROM 'hf://dataset/file.parquet'")
```

### Configuration

```python
from dr_duck.configs import AuthSettings, Paths

# Resolve tokens from .env files
auth = AuthSettings()
hf_token = auth.resolve("hf")
md_token = auth.resolve("motherduck")

# Manage paths
paths = Paths()
```

### Utilities

```python
from dr_duck.utils import (
    add_marimo_display,      # Decorator for marimo notebook integration
    iter_file_glob_from_roots,  # Recursive file globbing
    ensure_column,           # DataFrame column utilities
    fill_missing_values,
    rename_columns,
)

from dr_duck import (
    is_nully,               # Check for null-like values
    normalize_str,          # String normalization
    convert_timestamp,      # Timestamp conversion
    TaskArtifactType,       # Enum for artifact types
)
```

## Modules

- `dr_duck.motherduck` - MotherDuck connection helpers
- `dr_duck.hf` - HuggingFace I/O and location management
- `dr_duck.configs` - Authentication and path configuration
- `dr_duck.utils` - General utilities (pandas, I/O, display)
- `dr_duck.normalization` - String and timestamp normalization
- `dr_duck.types` - Shared type definitions

## License

MIT
