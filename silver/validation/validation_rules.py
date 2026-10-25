"""
Reusable, non-destructive data validation helpers for EHDP.

These functions report issues; they do not clean, delete, or modify input data.
Pass pandas DataFrames and explicit column names from the calling pipeline.
"""
from __future__ import annotations

from typing import Any, Iterable, Optional

import pandas as pd


def _result(
    check_name: str,
    passed: bool,
    failed_records: int = 0,
    details: str = "",
) -> dict[str, Any]:
    """Return a consistent, serializable validation result."""
    return {
        "check_name": check_name,
        "status": "PASS" if passed else "FAIL",
        "passed": bool(passed),
        "failed_records": int(failed_records),
        "details": details,
    }


def check_required_columns(
    df: pd.DataFrame,
    required_columns: Iterable[str],
    dataset_name: str = "dataset",
) -> dict[str, Any]:
    """Check that every named column exists in a DataFrame."""
    missing = sorted(set(required_columns) - set(df.columns))
    return _result(
        f"{dataset_name}: required columns",
        not missing,
        len(missing),
        "All required columns are present." if not missing
        else f"Missing columns: {', '.join(missing)}",
    )


def check_missing_values(
    df: pd.DataFrame,
    columns: Optional[Iterable[str]] = None,
    dataset_name: str = "dataset",
) -> dict[str, Any]:
    """
    Count missing cells in selected columns.

    If columns is None, all DataFrame columns are checked. A column's missing
    cell count is reported in details; failed_records is the total missing cells.
    """
    selected = list(columns) if columns is not None else list(df.columns)
    absent = sorted(set(selected) - set(df.columns))
    if absent:
        return _result(
            f"{dataset_name}: missing values",
            False,
            len(absent),
            f"Requested columns do not exist: {', '.join(absent)}",
        )

    counts = df[selected].isna().sum()
    nonzero = {str(col): int(count) for col, count in counts.items() if count > 0}
    total = int(counts.sum())
    return _result(
        f"{dataset_name}: missing values",
        total == 0,
        total,
        "No missing values in checked columns." if not nonzero
        else f"Missing cells by column: {nonzero}",
    )


def check_duplicate_rows(
    df: pd.DataFrame,
    subset: Optional[Iterable[str]] = None,
    dataset_name: str = "dataset",
) -> dict[str, Any]:
    """
    Count duplicate rows, or duplicates based on a selected key/subset.

    pandas duplicated() marks later occurrences as duplicates, not the first row.
    """
    selected = list(subset) if subset is not None else None
    if selected is not None:
        absent = sorted(set(selected) - set(df.columns))
        if absent:
            return _result(
                f"{dataset_name}: duplicate check",
                False,
                len(absent),
                f"Key columns do not exist: {', '.join(absent)}",
            )
        if not selected:
            return _result(
                f"{dataset_name}: duplicate check",
                False,
                1,
                "No key columns were supplied.",
            )

    duplicate_count = int(df.duplicated(subset=selected).sum())
    label = ", ".join(selected) if selected is not None else "all columns"
    return _result(
        f"{dataset_name}: duplicate check",
        duplicate_count == 0,
        duplicate_count,
        f"Duplicate rows checked using {label}: {duplicate_count}.",
    )


def check_unique_key(
    df: pd.DataFrame,
    key_column: str,
    dataset_name: str = "dataset",
    allow_nulls: bool = False,
) -> dict[str, Any]:
    """Check key uniqueness and, by default, reject null key values."""
    if key_column not in df.columns:
        return _result(
            f"{dataset_name}: unique key {key_column}",
            False,
            1,
            f"Key column '{key_column}' does not exist.",
        )

    null_count = int(df[key_column].isna().sum())
    duplicate_count = int(df[key_column].dropna().duplicated().sum())
    failed = duplicate_count + (0 if allow_nulls else null_count)
    details = (
        f"duplicate non-null keys={duplicate_count}; null keys={null_count}; "
        f"allow_nulls={allow_nulls}"
    )
    return _result(
        f"{dataset_name}: unique key {key_column}",
        failed == 0,
        failed,
        details,
    )


def check_date_order(
    df: pd.DataFrame,
    start_column: str,
    end_column: str,
    dataset_name: str = "dataset",
    allow_open_ended: bool = True,
) -> dict[str, Any]:
    """
    Check that end dates are not earlier than start dates.

    Unparseable non-null values are counted as failures. If allow_open_ended is
    True, null end dates are permitted (for example, an ongoing device record).
    Null start dates are not independently rejected by this check.
    """
    missing_columns = [
        col for col in (start_column, end_column) if col not in df.columns
    ]
    if missing_columns:
        return _result(
            f"{dataset_name}: date order",
            False,
            len(missing_columns),
            f"Missing date columns: {', '.join(missing_columns)}",
        )

    start_raw = df[start_column]
    end_raw = df[end_column]
    start = pd.to_datetime(start_raw, errors="coerce")
    end = pd.to_datetime(end_raw, errors="coerce")

    bad_start_parse = start_raw.notna() & start.isna()
    bad_end_parse = end_raw.notna() & end.isna()
    reversed_dates = start.notna() & end.notna() & (end < start)
    disallowed_open_end = (
        end.isna() & end_raw.isna() & (not allow_open_ended)
    )
    failed_mask = bad_start_parse | bad_end_parse | reversed_dates | disallowed_open_end
    failed = int(failed_mask.sum())

    details = (
        f"reversed date pairs={int(reversed_dates.sum())}; "
        f"unparseable start values={int(bad_start_parse.sum())}; "
        f"unparseable end values={int(bad_end_parse.sum())}; "
        f"null end dates={int((end_raw.isna()).sum())}; "
        f"allow_open_ended={allow_open_ended}"
    )
    return _result(
        f"{dataset_name}: date order {start_column} <= {end_column}",
        failed == 0,
        failed,
        details,
    )


def check_foreign_key(
    child_df: pd.DataFrame,
    child_column: str,
    parent_df: pd.DataFrame,
    parent_column: str,
    relationship_name: Optional[str] = None,
    allow_nulls: bool = True,
) -> dict[str, Any]:
    """
    Check whether non-null child key values exist in the parent key column.

    Null child values are allowed by default, which suits optional relationships.
    This checks key membership; it does not enforce database constraints.
    """
    label = relationship_name or f"{child_column} -> {parent_column}"
    if child_column not in child_df.columns:
        return _result(label, False, 1, f"Child column '{child_column}' is missing.")
    if parent_column not in parent_df.columns:
        return _result(label, False, 1, f"Parent column '{parent_column}' is missing.")

    child_values = child_df[child_column]
    parent_values = set(parent_df[parent_column].dropna().tolist())
    null_mask = child_values.isna()
    orphan_mask = (~null_mask) & (~child_values.isin(parent_values))
    null_failures = int(null_mask.sum()) if not allow_nulls else 0
    orphan_count = int(orphan_mask.sum())
    failed = orphan_count + null_failures

    return _result(
        label,
        failed == 0,
        failed,
        f"orphan child rows={orphan_count}; null child keys={int(null_mask.sum())}; "
        f"allow_nulls={allow_nulls}",
    )


def validate_dataframe(
    df: pd.DataFrame,
    dataset_name: str,
    required_columns: Optional[Iterable[str]] = None,
    unique_key: Optional[str] = None,
    check_all_missing_values: bool = False,
    duplicate_subset: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """
    Run a small configurable set of common checks and return a results DataFrame.

    This function intentionally does not assume every column must be non-null:
    configure required columns and unique keys according to the source contract.
    """
    results: list[dict[str, Any]] = []

    if required_columns is not None:
        results.append(check_required_columns(df, required_columns, dataset_name))

    if unique_key is not None:
        results.append(check_unique_key(df, unique_key, dataset_name))

    if duplicate_subset is not None:
        results.append(check_duplicate_rows(df, duplicate_subset, dataset_name))

    if check_all_missing_values:
        results.append(check_missing_values(df, dataset_name=dataset_name))

    return pd.DataFrame(
        results,
        columns=["check_name", "status", "passed", "failed_records", "details"],
    )


def results_to_csv(results: pd.DataFrame, output_path: str) -> None:
    """Write validation results to CSV without an implicit DataFrame index."""
    results.to_csv(output_path, index=False)
