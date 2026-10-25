import pandas as pd

from validation_rules import (
    check_date_order,
    check_foreign_key,
    check_unique_key,
    validate_dataframe,
)


def test_unique_key_detects_duplicates():
    df = pd.DataFrame({"patient_id": ["p1", "p1", "p2"]})
    result = check_unique_key(df, "patient_id", "patients")
    assert result["status"] == "FAIL"
    assert result["failed_records"] == 1


def test_date_order_allows_open_ended_records_by_default():
    df = pd.DataFrame({
        "start": ["2025-01-01", "2025-02-01"],
        "stop": ["2025-01-02", None],
    })
    result = check_date_order(df, "start", "stop", "devices")
    assert result["status"] == "PASS"


def test_date_order_detects_reversed_dates():
    df = pd.DataFrame({"start": ["2025-02-02"], "stop": ["2025-02-01"]})
    result = check_date_order(df, "start", "stop")
    assert result["status"] == "FAIL"
    assert result["failed_records"] == 1


def test_foreign_key_detects_orphan():
    child = pd.DataFrame({"patient_id": ["p1", "missing"]})
    parent = pd.DataFrame({"id": ["p1", "p2"]})
    result = check_foreign_key(child, "patient_id", parent, "id")
    assert result["status"] == "FAIL"
    assert result["failed_records"] == 1


def test_dataframe_validation_returns_table():
    df = pd.DataFrame({"id": ["a", "b"], "name": ["x", "y"]})
    result = validate_dataframe(
        df, "sample", required_columns=["id", "name"], unique_key="id"
    )
    assert len(result) == 2
    assert result["passed"].all()
