from __future__ import annotations

import tempfile
from pathlib import Path

import duckdb
import pandas as pd
import pytest

from dr_duck import (
    create_table_from_df,
    describe_table,
    insert_df,
    list_tables,
    query_parquet,
    query_to_df,
)


@pytest.fixture
def conn() -> duckdb.DuckDBPyConnection:
    return duckdb.connect(":memory:")


@pytest.fixture
def sample_df() -> pd.DataFrame:
    return pd.DataFrame({"id": [1, 2, 3], "name": ["alice", "bob", "charlie"]})


class TestQueryToDf:
    def test_basic_query(self, conn: duckdb.DuckDBPyConnection) -> None:
        conn.execute("CREATE TABLE test (x INT, y TEXT)")
        conn.execute("INSERT INTO test VALUES (1, 'a'), (2, 'b')")

        result = query_to_df(conn, "SELECT * FROM test")

        assert len(result) == 2
        assert list(result.columns) == ["x", "y"]
        assert result["x"].tolist() == [1, 2]

    def test_with_where_clause(self, conn: duckdb.DuckDBPyConnection) -> None:
        conn.execute("CREATE TABLE test (x INT)")
        conn.execute("INSERT INTO test VALUES (1), (2), (3)")

        result = query_to_df(conn, "SELECT * FROM test WHERE x > 1")

        assert len(result) == 2
        assert result["x"].tolist() == [2, 3]


class TestQueryParquet:
    def test_query_parquet_file(self, conn: duckdb.DuckDBPyConnection) -> None:
        df = pd.DataFrame({"a": [10, 20], "b": ["x", "y"]})

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.parquet"
            df.to_parquet(path)

            result = query_parquet(conn, str(path))

            assert len(result) == 2
            assert result["a"].tolist() == [10, 20]

    def test_query_parquet_with_sql(self, conn: duckdb.DuckDBPyConnection) -> None:
        df = pd.DataFrame({"val": [1, 2, 3, 4, 5]})

        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test.parquet"
            df.to_parquet(path)

            result = query_parquet(conn, str(path), sql="SELECT * FROM {table} WHERE val > 2")

            assert len(result) == 3
            assert result["val"].tolist() == [3, 4, 5]


class TestListTables:
    def test_empty_database(self, conn: duckdb.DuckDBPyConnection) -> None:
        result = list_tables(conn)
        assert len(result) == 0

    def test_with_tables(self, conn: duckdb.DuckDBPyConnection) -> None:
        conn.execute("CREATE TABLE foo (x INT)")
        conn.execute("CREATE TABLE bar (y TEXT)")

        result = list_tables(conn)

        assert len(result) == 2
        assert set(result["name"].tolist()) == {"foo", "bar"}


class TestDescribeTable:
    def test_describe_columns(self, conn: duckdb.DuckDBPyConnection) -> None:
        conn.execute("CREATE TABLE test (id INTEGER, name VARCHAR, score DOUBLE)")

        result = describe_table(conn, "test")

        assert len(result) == 3
        assert result["column_name"].tolist() == ["id", "name", "score"]


class TestInsertDf:
    def test_insert_into_existing_table(
        self, conn: duckdb.DuckDBPyConnection, sample_df: pd.DataFrame
    ) -> None:
        conn.execute("CREATE TABLE test (id INTEGER, name VARCHAR)")

        insert_df(conn, sample_df, "test")

        result = conn.execute("SELECT * FROM test").df()
        assert len(result) == 3
        assert result["name"].tolist() == ["alice", "bob", "charlie"]

    def test_insert_multiple_times(
        self, conn: duckdb.DuckDBPyConnection, sample_df: pd.DataFrame
    ) -> None:
        conn.execute("CREATE TABLE test (id INTEGER, name VARCHAR)")

        insert_df(conn, sample_df, "test")
        insert_df(conn, sample_df, "test")

        result = conn.execute("SELECT COUNT(*) as cnt FROM test").df()
        assert result["cnt"].iloc[0] == 6


class TestCreateTableFromDf:
    def test_create_new_table(
        self, conn: duckdb.DuckDBPyConnection, sample_df: pd.DataFrame
    ) -> None:
        create_table_from_df(conn, sample_df, "new_table")

        result = conn.execute("SELECT * FROM new_table").df()
        assert len(result) == 3
        assert list(result.columns) == ["id", "name"]

    def test_create_with_replace(
        self, conn: duckdb.DuckDBPyConnection, sample_df: pd.DataFrame
    ) -> None:
        create_table_from_df(conn, sample_df, "test_table")

        new_df = pd.DataFrame({"id": [99], "name": ["new"]})
        create_table_from_df(conn, new_df, "test_table", replace=True)

        result = conn.execute("SELECT * FROM test_table").df()
        assert len(result) == 1
        assert result["id"].iloc[0] == 99

    def test_create_without_replace_fails(
        self, conn: duckdb.DuckDBPyConnection, sample_df: pd.DataFrame
    ) -> None:
        create_table_from_df(conn, sample_df, "test_table")

        with pytest.raises(duckdb.CatalogException):
            create_table_from_df(conn, sample_df, "test_table", replace=False)
