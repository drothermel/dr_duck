# dr-duck

DuckDB and MotherDuck utilities with autocomplete-friendly helpers.

## Installation

```bash
pip install dr-duck
```

Or with uv:
```bash
uv add dr-duck
```

## Connection Helpers

```python
from dr_duck import open_motherduck_connection, open_local_connection

# MotherDuck (reads MOTHERDUCK_TOKEN from env)
conn = open_motherduck_connection()

# Local DuckDB file
conn = open_local_connection("my_data.duckdb")

# In-memory
conn = open_local_connection()  # defaults to :memory:

# With .env file and optional secrets
conn = open_local_connection(
    "data.duckdb",
    env_file=".env",
    hf_token="...",      # or reads HF_TOKEN from env
    s3_key_id="...",     # or reads AWS_ACCESS_KEY_ID from env
    s3_secret="...",     # or reads AWS_SECRET_ACCESS_KEY from env
)
```

## Secret Setup

```python
from dr_duck import setup_hf_secret, setup_s3_secret

# Set up HuggingFace secret (enables hf:// URLs)
setup_hf_secret(conn, token="...")  # or reads HF_TOKEN from env

# Set up S3 secret
setup_s3_secret(
    conn,
    key_id="...",        # or reads AWS_ACCESS_KEY_ID
    secret="...",        # or reads AWS_SECRET_ACCESS_KEY
    region="us-west-2",  # or reads AWS_REGION, defaults to us-east-1
    endpoint="...",      # optional, for S3-compatible services
)
```

## Query Helpers

```python
from dr_duck import query_to_df, query_hf, query_parquet, list_tables, describe_table

# Run any SQL, get DataFrame
df = query_to_df(conn, "SELECT * FROM my_table LIMIT 10")

# Query HuggingFace dataset
df = query_hf(conn, "username/dataset", "data/*.parquet")
df = query_hf(conn, "username/dataset", "train.parquet", sql="SELECT * FROM {table} WHERE x > 5")

# Query parquet file (local or remote)
df = query_parquet(conn, "s3://bucket/data.parquet")
df = query_parquet(conn, "data/*.parquet", sql="SELECT col1, col2 FROM {table}")

# Schema inspection
tables = list_tables(conn)
schema = describe_table(conn, "my_table")
```

## DataFrame Helpers

```python
from dr_duck import insert_df, create_table_from_df

# Insert DataFrame into existing table
insert_df(conn, df, "my_table")

# Create new table from DataFrame
create_table_from_df(conn, df, "new_table")
create_table_from_df(conn, df, "new_table", replace=True)  # CREATE OR REPLACE
```

## Environment Variables

- `MOTHERDUCK_TOKEN` - Required for `open_motherduck_connection`
- `HF_TOKEN` - Enables `hf://` URLs in DuckDB queries
- `AWS_ACCESS_KEY_ID` - For S3 access
- `AWS_SECRET_ACCESS_KEY` - For S3 access
- `AWS_REGION` - S3 region (defaults to us-east-1)

## License

MIT
