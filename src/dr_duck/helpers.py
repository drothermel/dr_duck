from __future__ import annotations

import duckdb
import pandas as pd

__all__ = [
    "query_to_df",
    "query_hf",
    "query_parquet",
    "list_tables",
    "describe_table",
    "insert_df",
    "create_table_from_df",
]


def query_to_df(conn: duckdb.DuckDBPyConnection, sql: str) -> pd.DataFrame:
    return conn.execute(sql).df()


def query_hf(
    conn: duckdb.DuckDBPyConnection,
    repo_id: str,
    path: str = "**/*.parquet",
    *,
    sql: str | None = None,
) -> pd.DataFrame:
    hf_url = f"hf://{repo_id}/{path}"
    if sql:
        full_sql = sql.replace("{table}", f"'{hf_url}'")
    else:
        full_sql = f"SELECT * FROM '{hf_url}'"
    return conn.execute(full_sql).df()


def query_parquet(
    conn: duckdb.DuckDBPyConnection,
    path: str,
    *,
    sql: str | None = None,
) -> pd.DataFrame:
    if sql:
        full_sql = sql.replace("{table}", f"'{path}'")
    else:
        full_sql = f"SELECT * FROM '{path}'"
    return conn.execute(full_sql).df()


def list_tables(conn: duckdb.DuckDBPyConnection) -> pd.DataFrame:
    return conn.execute("SHOW TABLES").df()


def describe_table(conn: duckdb.DuckDBPyConnection, table: str) -> pd.DataFrame:
    return conn.execute(f"DESCRIBE {table}").df()


def insert_df(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
    table: str,
) -> None:
    conn.register("_dr_duck_temp_df", df)
    conn.execute(f"INSERT INTO {table} SELECT * FROM _dr_duck_temp_df")
    conn.unregister("_dr_duck_temp_df")


def create_table_from_df(
    conn: duckdb.DuckDBPyConnection,
    df: pd.DataFrame,
    table: str,
    *,
    replace: bool = False,
) -> None:
    conn.register("_dr_duck_temp_df", df)
    create_stmt = "CREATE OR REPLACE TABLE" if replace else "CREATE TABLE"
    conn.execute(f"{create_stmt} {table} AS SELECT * FROM _dr_duck_temp_df")
    conn.unregister("_dr_duck_temp_df")
