"""Bronze-layer JSON ingestion for the UC2 healthcare data platform.

Reads JSON files and appends their unmodified records to PostgreSQL tables in
the bronze schema. Supports JSON arrays/objects and newline-delimited JSON
(JSONL/NDJSON). This is ingestion only; cleaning belongs in the Silver layer.

Dependencies: pandas, SQLAlchemy, psycopg2-binary
Example (PowerShell):
  $env:UC2_DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@localhost:5432/uc2"
  python bronze/ingestion/ingest_json_sources.py --source-dir data/bronze/json
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, text

LOGGER = logging.getLogger("uc2.bronze.json")
IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def safe_identifier(value: str, label: str) -> str:
    if not IDENTIFIER_RE.fullmatch(value):
        raise ValueError(f"Invalid {label} {value!r}. Use letters, digits, and underscores; start with a letter or underscore.")
    return value


def read_json_records(path: Path, lines: bool) -> pd.DataFrame:
    """Parse JSON records into a tabular DataFrame without doing data cleaning."""
    if lines:
        frame = pd.read_json(path, lines=True, dtype=False)
    else:
        with path.open("r", encoding="utf-8-sig") as handle:
            payload = json.load(handle)
        if isinstance(payload, list):
            records = payload
        elif isinstance(payload, dict):
            # A single object is treated as one source record. Nested structures
            # remain JSON-like values where possible instead of being flattened.
            records = [payload]
        else:
            raise ValueError("JSON root must be an object or an array of objects. Use --lines for NDJSON files.")
        if not all(isinstance(record, dict) for record in records):
            raise ValueError("JSON arrays must contain objects (one object per record).")
        frame = pd.DataFrame.from_records(records)
    return frame


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest JSON files into the UC2 PostgreSQL Bronze schema.")
    parser.add_argument("--source-dir", default="data/bronze/json", help="Folder containing JSON files (default: data/bronze/json).")
    parser.add_argument("--schema", default="bronze", help="PostgreSQL destination schema (default: bronze).")
    parser.add_argument("--lines", action="store_true", help="Read newline-delimited JSON (JSONL/NDJSON).")
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
    files = sorted(p for p in source_dir.iterdir() if p.is_file() and p.suffix.lower() in {".json", ".jsonl", ".ndjson"})
    if not files:
        LOGGER.warning("No JSON files found in %s", source_dir.resolve())
        return 0

    try:
        engine = create_engine(args.database_url, pool_pre_ping=True)
        with engine.begin() as connection:
            connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS "{args.schema}"'))
        failures = 0
        for path in files:
            try:
                target = safe_identifier(path.stem, "target table name")
                is_lines = args.lines or path.suffix.lower() in {".jsonl", ".ndjson"}
                frame = read_json_records(path, is_lines)
                if frame.empty and len(frame.columns) == 0:
                    LOGGER.warning("Skipping empty JSON file with no records/fields: %s", path.name)
                    continue
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
                LOGGER.exception("Failed to ingest JSON file: %s", path.name)
        engine.dispose()
        if failures:
            LOGGER.error("Completed with %d failed file(s) out of %d.", failures, len(files))
            return 1
        LOGGER.info("JSON ingestion completed successfully for %d file(s).", len(files))
        return 0
    except Exception:
        LOGGER.exception("JSON ingestion setup failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
