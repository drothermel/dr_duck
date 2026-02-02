# dr-duck

Simple MotherDuck connection utilities with optional HuggingFace token setup.

## Installation

```bash
pip install dr-duck
```

Or with uv:
```bash
uv add dr-duck
```

## Usage

```python
from dr_duck import open_motherduck_connection

# Reads MOTHERDUCK_TOKEN and HF_TOKEN from environment
conn = open_motherduck_connection()

# Or specify an .env file
conn = open_motherduck_connection(env_file=".env")

# Or pass tokens directly
conn = open_motherduck_connection(
    motherduck_token="your_token",
    hf_token="your_hf_token",  # optional, enables hf:// URLs in DuckDB
)

# Use the connection
result = conn.execute("SELECT * FROM my_table").df()
```

## Environment Variables

- `MOTHERDUCK_TOKEN` - Required for MotherDuck connection
- `HF_TOKEN` - Optional, enables querying HuggingFace datasets via `hf://` URLs

## License

MIT
