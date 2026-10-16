"""Checks that the 15 UC2 raw tables exist.
Set UC2_TEST_DATABASE_URL to run database-backed tests.
"""
import os
import pytest

DATABASE_URL = os.getenv("UC2_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not DATABASE_URL, reason="Set UC2_TEST_DATABASE_URL to run database tests")

def test_required_raw_tables_exist():
    from sqlalchemy import create_engine, text
    expected = {
        "uc2_patients", "uc2_encounters", "uc2_conditions", "uc2_observations",
        "uc2_medications", "uc2_procedures", "uc2_allergies", "uc2_immunizations",
        "uc2_careplans", "uc2_devices", "uc2_imaging_studies", "uc2_organizations",
        "uc2_payer_transitions", "uc2_payers", "uc2_providers"
    }
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'")).fetchall()
    actual = {row[0] for row in rows}
    assert expected.issubset(actual), f"Missing raw tables: {sorted(expected - actual)}"
