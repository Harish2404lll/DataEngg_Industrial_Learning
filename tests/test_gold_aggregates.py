"""Smoke tests for Gold views. Set UC2_TEST_DATABASE_URL to run."""
import os
import pytest

DATABASE_URL = os.getenv("UC2_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="Set UC2_TEST_DATABASE_URL to run database tests")

def test_gold_views_exist():
    from sqlalchemy import create_engine, text
    expected = {
        "dim_patients", "dim_providers_organizations", "dim_clinical_codes", "dim_devices",
        "fct_encounters", "fct_patient_observations", "fct_medications_immunizations",
        "fct_imaging_procedures", "mrt_patient_health_summary", "mrt_careplan_outcomes"
    }
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT table_name FROM information_schema.views WHERE table_schema='gold'")).fetchall()
    actual = {row[0] for row in rows}
    assert expected.issubset(actual), f"Missing Gold views: {sorted(expected - actual)}"
