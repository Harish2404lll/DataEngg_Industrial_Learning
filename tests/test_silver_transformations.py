"""Small, beginner-friendly tests for Silver cleansing rules."""
import pandas as pd

def test_gender_standardization():
    source = pd.Series(["M", "male", "F", "female", None])
    normalized = source.astype("string").str.strip().str.lower().replace({"m": "male", "f": "female"})
    assert normalized.iloc[0] == "male"
    assert normalized.iloc[1] == "male"
    assert normalized.iloc[2] == "female"
    assert normalized.iloc[3] == "female"
    assert pd.isna(normalized.iloc[4])

def test_stop_before_start_is_flagged():
    df = pd.DataFrame({
        "start_date": pd.to_datetime(["2025-01-02", "2025-01-01"]),
        "stop_date": pd.to_datetime(["2025-01-01", "2025-01-02"])
    })
    invalid = df["stop_date"].notna() & (df["stop_date"] < df["start_date"])
    assert invalid.tolist() == [True, False]

def test_observation_duplicates_can_be_identified():
    df = pd.DataFrame({"patient_id": ["p1", "p1"], "code": ["x", "x"], "value": ["1", "1"]})
    assert int(df.duplicated().sum()) == 1
