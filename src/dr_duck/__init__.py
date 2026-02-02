from dr_duck.connection import (
    open_local_connection,
    open_motherduck_connection,
    setup_hf_secret,
    setup_s3_secret,
)
from dr_duck.helpers import (
    create_table_from_df,
    describe_table,
    insert_df,
    list_tables,
    query_hf,
    query_parquet,
    query_to_df,
)

__all__ = [
    "create_table_from_df",
    "describe_table",
    "insert_df",
    "list_tables",
    "open_local_connection",
    "open_motherduck_connection",
    "query_hf",
    "query_parquet",
    "query_to_df",
    "setup_hf_secret",
    "setup_s3_secret",
]
