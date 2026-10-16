"""Bronze-layer CSV ingestion for the UC2 healthcare data platform.

Reads CSV files and appends their unmodified rows to PostgreSQL tables in the
bronze schema. This is ingestion only: do not clean or standardize data here.

Dependencies: pandas, SQLAlchemy, psycopg2-binary
Example (PowerShell):
  $env:UC2_DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@localhost:5432/uc2"
  python bronze/ingestion/ingest_csv_sources.py --source-dir data/bronze/csv

By default, each file name becomes its target table name (patients.csv ->
bronze.patients). Use --mapping to supply a JSON mapping file when source names
differ from your desired target table names. See the README created alongside
these scripts for details.
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL, make_url

LOGGER = logging.getLogger("uc2.bronze.csv")
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def safe_identifier(value: str, label: str) -> str:
    """Reject SQL identifiers that could be unsafe or invalid."""
    if not IDENTIFIER_RE.fullmatch(value):
        raise ValueError(f"Invalid {label} {value!r}. Use letters, digits, and underscores; start with a letter or underscore.")
    return value


def load_mapping(mapping_path: Path | None) -> dict[str, str]:
    """Load optional mapping JSON: {"source.csv": "target_table"}."""
    if mapping_path is None:
        return {}
    with mapping_path.open("r", encoding="utf-8") as handle:
        mapping = json.load(handle)
    if not isinstance(mapping, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in mapping.items()):
        raise ValueError("Mapping JSON must be an object of filename-to-table-name strings.")
    return mapping


def read_csv(path: Path, encoding: str) -> pd.DataFrame:
    """Read a CSV while preserving source values as much as pandas permits."""
    try:
        return pd.read_csv(path, encoding=encoding, dtype=object, keep_default_na=False)
    except UnicodeDecodeError:
        if encoding.lower().replace("-", "") != "utf8":
            raise
        LOGGER.warning("UTF-8 decoding failed for %s; retrying with UTF-8 BOM support.", path.name)
        return pd.read_csv(path, encoding="utf-8-sig", dtype=object, keep_default_na=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest CSV files into the UC2 PostgreSQL Bronze schema.")
    parser.add_argument("--source-dir", default="data/bronze/csv", help="Folder containing CSV files (default: data/bronze/csv).")
    parser.add_argument("--schema", default="bronze", help="PostgreSQL destination schema (default: bronze).")
    parser.add_argument("--mapping", type=Path, help="Optional JSON mapping file: {\"patients.csv\": \"uc2_patients\"}.")
    parser.add_argument("--encoding", default="utf-8", help="CSV encoding (default: utf-8).")
    parser.add_argument("--if-exists", choices=("append", "replace", "fail"), default="append", help="Table behavior (default: append).")
    parser.add_argument("--chunksize", type=int, default=5000, help="Rows inserted per batch (default: 5000).")
    parser.add_argument("--database-url", default=os.getenv("UC2_DATABASE_URL"), help="SQLAlchemy PostgreSQL URL; preferably set UC2_DATABASE_URL.")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    safe_identifier(args.schema, "schema name")
    if args.chunksize < 1:
        parser.error("--chunksize must be at least 1")
    if not args.database_url:
        LOGGER.error("Database URL missing. Set UC2_DATABASE_URL or pass --database-url.")
        return 2

    source_dir = Path(args.source_dir)
    if not source_dir.is_dir():
        LOGGER.error("Source directory does not exist: %s", source_dir.resolve())
        return 2
    files = sorted(p for p in source_dir.glob("*.csv") if p.is_file())
    if not files:
        LOGGER.warning("No CSV files found in %s", source_dir.resolve())
        return 0

    try:
        mapping = load_mapping(args.mapping)
        engine = create_engine(args.database_url, pool_pre_ping=True)
        with engine.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{args.schema}"'))

        failures = 0
        for path in files:
            try:
                target = safe_identifier(mapping.get(path.name, path.stem), "target table name")
                frame = read_csv(path, args.encoding)
                if len(frame.columns) == 0:
                    raise ValueError("CSV has no header/columns")
                # Add ingestion metadata without changing the original source fields.
                frame["_source_file"] = path.name
                frame["_ingested_at_utc"] = pd.Timestamp.now(tz="UTC")
                frame.to_sql(
                    name=target,
                    con=engine,
                    schema=args.schema,
                    if_exists=args.if_exists,
                    index=False,
                    chunksize=args.chunksize,
                    method="multi",
                )
                LOGGER.info("Ingested %s rows from %s into %s.%s", len(frame), path.name, args.schema, target)
            except Exception:
                failures += 1
                LOGGER.exception("Failed to ingest CSV file: %s", path.name)
        engine.dispose()
        if failures:
            LOGGER.error("Completed with %d failed file(s) out of %d.", failures, len(files))
            return 1
        LOGGER.info("CSV ingestion completed successfully for %d file(s).", len(files))
        return 0
    except Exception:
        LOGGER.exception("CSV ingestion setup failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
