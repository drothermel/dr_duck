from __future__ import annotations

import os
from pathlib import Path

import duckdb
from dotenv import load_dotenv

__all__ = [
    "open_local_connection",
    "open_motherduck_connection",
    "setup_hf_secret",
    "setup_s3_secret",
]


def open_local_connection(
    path: Path | str = ":memory:",
    *,
    env_file: Path | str | None = None,
    hf_token: str | None = None,
    s3_key_id: str | None = None,
    s3_secret: str | None = None,
    s3_region: str | None = None,
) -> duckdb.DuckDBPyConnection:
    if env_file:
        load_dotenv(env_file)

    conn = duckdb.connect(str(path))

    hf = hf_token or os.environ.get("HF_TOKEN")
    if hf:
        setup_hf_secret(conn, token=hf)

    if s3_key_id or s3_secret or os.environ.get("AWS_ACCESS_KEY_ID"):
        setup_s3_secret(
            conn,
            key_id=s3_key_id,
            secret=s3_secret,
            region=s3_region,
        )

    return conn


def open_motherduck_connection(
    *,
    env_file: Path | str | None = None,
    motherduck_token: str | None = None,
    hf_token: str | None = None,
    s3_key_id: str | None = None,
    s3_secret: str | None = None,
    s3_region: str | None = None,
) -> duckdb.DuckDBPyConnection:
    if env_file:
        load_dotenv(env_file)

    md_token = motherduck_token or os.environ.get("MOTHERDUCK_TOKEN")
    assert md_token, "MOTHERDUCK_TOKEN not found in environment or .env file"

    conn = duckdb.connect(f"md:?motherduck_token={md_token}")

    hf = hf_token or os.environ.get("HF_TOKEN")
    if hf:
        setup_hf_secret(conn, token=hf)

    if s3_key_id or s3_secret or os.environ.get("AWS_ACCESS_KEY_ID"):
        setup_s3_secret(
            conn,
            key_id=s3_key_id,
            secret=s3_secret,
            region=s3_region,
        )

    return conn


def setup_hf_secret(
    conn: duckdb.DuckDBPyConnection,
    *,
    token: str | None = None,
) -> None:
    hf = token or os.environ.get("HF_TOKEN")
    assert hf, "HF_TOKEN not found in environment"
    conn.execute(
        f"""
        CREATE SECRET IF NOT EXISTS hf_token (
            TYPE HUGGINGFACE,
            TOKEN '{hf}'
        );
        """
    )


def setup_s3_secret(
    conn: duckdb.DuckDBPyConnection,
    *,
    key_id: str | None = None,
    secret: str | None = None,
    region: str | None = None,
    endpoint: str | None = None,
    url_style: str | None = None,
) -> None:
    aws_key = key_id or os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret = secret or os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = region or os.environ.get("AWS_REGION", "us-east-1")

    assert aws_key, "AWS_ACCESS_KEY_ID not found in environment"
    assert aws_secret, "AWS_SECRET_ACCESS_KEY not found in environment"

    secret_parts = [
        "TYPE S3",
        f"KEY_ID '{aws_key}'",
        f"SECRET '{aws_secret}'",
        f"REGION '{aws_region}'",
    ]

    if endpoint:
        secret_parts.append(f"ENDPOINT '{endpoint}'")
    if url_style:
        secret_parts.append(f"URL_STYLE '{url_style}'")

    conn.execute(
        f"""
        CREATE SECRET IF NOT EXISTS s3_secret (
            {", ".join(secret_parts)}
        );
        """
    )
