"""
EHDP Sprint 2: Data profiling, quality checks, and Silver-layer cleaning.

Run from any working directory:
    python python/data_profiling.py

Source data stays unchanged in /datasets.
Cleaned CSV files are written to /silver/cleansing.
Reports are written to /docs/sprint2/data_profiling/reports.
"""

from pathlib import Path
import json
import warnings

import pandas as pd

try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = PROJECT_ROOT / "datasets"
SILVER_PATH = PROJECT_ROOT / "silver" / "cleansing"
REPORT_PATH = PROJECT_ROOT / "docs" / "sprint2" / "data_profiling" / "reports"
PLOT_PATH = PROJECT_ROOT / "docs" / "sprint2" / "data_profiling" / "visualizations"

SOURCE_FILES = {
    "Patients": "patients.json",
    "Encounters": "encounters.csv",
    "Conditions": "conditions.csv",
    "Observations": "observations.csv",
    "Medications": "medications.json",
    "Procedures": "procedures.csv",
    "Allergies": "allergies.json",
    "Immunizations": "immunizations.csv",
    "Organizations": "organizations.csv",
    "Payers": "payers.json",
    "Providers": "providers.csv",
    "Payer Transitions": "payer_transitions.json",
    "Careplans": "careplans.csv",
    "Devices": "devices.csv",
    "Imaging Studies": "imaging_studies.json",
}

DATE_COLUMNS = {"BIRTHDATE", "DEATHDATE", "START", "STOP", "DATE"}
ID_COLUMNS = {"Id", "PATIENT", "ENCOUNTER", "ORGANIZATION", "PROVIDER", "PAYER"}
NON_NEGATIVE_KEYWORDS = (
    "COST", "CLAIM", "REVENUE", "EXPENSE", "CHARGE",
    "COVERED", "UNCOVERED", "COVERAGE",
)


def load_datasets():
    """Load the source CSV/JSON files without modifying the originals."""
    loaded = {}
    for dataset_name, filename in SOURCE_FILES.items():
        file_path = DATA_PATH / filename
        if not file_path.exists():
            raise FileNotFoundError(
                f"Required source file not found: {file_path}\n"
                "Check that the Synthea files are in the repository's datasets folder."
            )

        if file_path.suffix.lower() == ".csv":
            frame = pd.read_csv(file_path, low_memory=False)
        elif file_path.suffix.lower() == ".json":
            frame = pd.read_json(file_path)
        else:
            raise ValueError(f"Unsupported source format: {file_path.suffix}")

        # Remove accidental spaces from headers while retaining source column names.
        frame.columns = [str(column).strip() for column in frame.columns]
        loaded[dataset_name] = frame

    return loaded


def count_missing_values(series):
    """Count nulls and blank strings without counting the same cell twice."""
    null_mask = series.isna()
    blank_mask = series.astype("string").str.strip().eq("").fillna(False)
    return int((null_mask | blank_mask).sum()), int(blank_mask.sum())


def make_reports(datasets):
    overview_rows = []
    column_rows = []
    missing_rows = []
    duplicate_rows = []
    id_rows = []
    categorical_rows = []
    numerical_rows = []
    outlier_rows = []
    patient_reference_rows = []
    relationship_rows = []
    date_rows = []
    date_range_rows = []
    business_rule_rows = []
    cleaned_duplicate_rows = []
    cleaned_validation_rows = []
    quality_rows = []

    # Profiling is performed against source data first.
    for name, frame in datasets.items():
        overview_rows.append({
            "Dataset": name, "Records": len(frame), "Columns": len(frame.columns)
        })
        duplicate_rows.append({
            "Dataset": name, "Duplicate Records": int(frame.duplicated().sum())
        })

        if "Id" in frame.columns:
            id_rows.append({
                "Dataset": name,
                "Missing IDs": int(frame["Id"].isna().sum()),
                "Duplicate IDs": int(frame["Id"].duplicated().sum()),
            })

        for column in frame.columns:
            missing_count, blank_count = count_missing_values(frame[column])
            column_rows.append({
                "Dataset": name,
                "Column": column,
                "Data Type": str(frame[column].dtype),
                "Non-Null Values": int(frame[column].notna().sum()),
                "Null Values": int(frame[column].isna().sum()),
                "Unique Values": int(frame[column].nunique(dropna=True)),
            })
            missing_rows.append({
                "Dataset": name,
                "Column": column,
                "Null Values": int(frame[column].isna().sum()),
                "Empty Strings": blank_count,
                "Total Missing": missing_count,
                "Missing Percentage": round(missing_count / len(frame) * 100, 2)
                if len(frame) else 0,
            })

            if (
                pd.api.types.is_object_dtype(frame[column])
                or pd.api.types.is_string_dtype(frame[column])
            ):
                non_null = frame[column].dropna().astype("string").str.strip()
                non_null = non_null[non_null.ne("")]
                counts = non_null.value_counts()
                if 0 < len(counts) <= 50:
                    categorical_rows.append({
                        "Dataset": name,
                        "Column": column,
                        "Unique_Values": int(len(counts)),
                        "Mode": str(counts.index[0]),
                        "Mode_Frequency": int(counts.iloc[0]),
                        "Mode_Percentage": round(counts.iloc[0] / len(non_null) * 100, 2),
                        "Rare_Categories_Under_1pct": int(
                            ((counts / len(non_null) * 100) < 1).sum()
                        ),
                    })

        for column in frame.select_dtypes(include="number").columns:
            values = frame[column].dropna()
            if values.empty:
                continue
            numerical_rows.append({
                "Dataset": name,
                "Column": column,
                "Count": int(values.count()),
                "Mean": values.mean(),
                "Std": values.std(),
                "Minimum": values.min(),
                "25%": values.quantile(0.25),
                "Median": values.median(),
                "75%": values.quantile(0.75),
                "Maximum": values.max(),
            })
            q1, q3 = values.quantile(0.25), values.quantile(0.75)
            iqr = q3 - q1
            lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
            count = int(((values < lower) | (values > upper)).sum())
            outlier_rows.append({
                "Dataset": name, "Column": column, "Q1": q1, "Q3": q3,
                "IQR": iqr, "Lower_Bound": lower, "Upper_Bound": upper,
                "Outlier_Count": count,
                "Outlier_Percentage": round(count / len(values) * 100, 2),
            })

        # Date quality checks. A blank STOP/DEATHDATE is often valid and is not
        # reported as an invalid date; nonblank values that fail parsing are.
        for column in frame.columns:
            if column.upper() not in DATE_COLUMNS:
                continue
            raw = frame[column]
            nonblank = raw.notna() & raw.astype("string").str.strip().ne("")
            parsed = pd.to_datetime(raw, errors="coerce")
            invalid = int((nonblank & parsed.isna()).sum())
            missing = int((~nonblank).sum())
            date_rows.append({
                "Dataset": name, "Date Column": column,
                "Invalid Nonblank Dates": invalid, "Missing Dates": missing,
            })

        for column in frame.columns:
            upper_name = column.upper()
            if any(keyword in upper_name for keyword in NON_NEGATIVE_KEYWORDS):
                numeric = pd.to_numeric(frame[column], errors="coerce")
                violations = int((numeric < 0).sum())
                business_rule_rows.append({
                    "Dataset": name, "Column": column,
                    "Rule": "Value should not be negative",
                    "Violations": violations,
                })

    # Validate foreign-key-like references against the raw source identifiers.
    id_sets = {}
    for name, frame in datasets.items():
        if "Id" in frame.columns:
            id_sets[name] = set(frame["Id"].dropna().astype(str).str.strip())

    patient_ids = id_sets.get("Patients", set())
    encounter_ids = id_sets.get("Encounters", set())
    organization_ids = id_sets.get("Organizations", set())
    provider_ids = id_sets.get("Providers", set())
    payer_ids = id_sets.get("Payers", set())

    for name, frame in datasets.items():
        checks = [
            ("PATIENT", patient_ids, "PATIENT"),
            ("ENCOUNTER", encounter_ids, "ENCOUNTER"),
            ("ORGANIZATION", organization_ids, "ORGANIZATION"),
            ("PROVIDER", provider_ids, "PROVIDER"),
            ("PAYER", payer_ids, "PAYER"),
        ]
        for column, valid_ids, label in checks:
            if column not in frame.columns or not valid_ids:
                continue
            values = frame[column].dropna().astype(str).str.strip()
            invalid = int((~values.isin(valid_ids)).sum())
            relationship_rows.append({
                "Dataset": name, "Reference Type": label,
                "Checked References": int(len(values)),
                "Invalid References": invalid,
            })
            if label == "PATIENT":
                patient_reference_rows.append({
                    "Dataset": name, "Invalid Patient References": invalid,
                })

    # Build Silver copies. Raw data is never overwritten.
    cleaned = {}
    for name, source in datasets.items():
        frame = source.copy()

        # Normalize whitespace and blank strings in text columns.
        for column in frame.columns:
            if (
                pd.api.types.is_object_dtype(frame[column])
                or pd.api.types.is_string_dtype(frame[column])
            ):
                frame[column] = frame[column].astype("string").str.strip()
                frame[column] = frame[column].replace("", pd.NA)

        # Normalize common identifiers and clinical code columns as strings.
        for column in ID_COLUMNS | {
            "CODE", "REASONCODE", "BODYSITE_CODE", "MODALITY_CODE",
        }:
            if column in frame.columns:
                frame[column] = frame[column].astype("string").str.strip()

        # Standardize date fields to datetime/ISO format on CSV export.
        for column in frame.columns:
            if column.upper() in DATE_COLUMNS:
                frame[column] = pd.to_datetime(frame[column], errors="coerce")

        # Standardize patient demographics without inventing missing values.
        if name == "Patients":
            if "GENDER" in frame.columns:
                frame["GENDER"] = frame["GENDER"].str.upper().replace({
                    "MALE": "M", "FEMALE": "F",
                })
            for column in ("MARITAL",):
                if column in frame.columns:
                    frame[column] = frame[column].str.upper()
            for column in ("RACE", "ETHNICITY", "CITY", "STATE"):
                if column in frame.columns:
                    frame[column] = frame[column].str.title()

        before = len(frame)
        frame = frame.drop_duplicates().copy()
        cleaned_duplicate_rows.append({
            "Dataset": name, "Records Before": before,
            "Records After": len(frame), "Duplicates Removed": before - len(frame),
        })
        missing_ids = int(frame["Id"].isna().sum()) if "Id" in frame.columns else "N/A"
        cleaned_validation_rows.append({
            "Dataset": name, "Records": len(frame),
            "Remaining Duplicates": int(frame.duplicated().sum()),
            "Missing IDs": missing_ids,
        })
        cleaned[name] = frame

    for name, source in datasets.items():
        clean_frame = cleaned[name]
        missing_total = sum(count_missing_values(source[col])[0] for col in source.columns)
        quality_rows.append({
            "Dataset": name,
            "Original Records": len(source),
            "Columns": len(source.columns),
            "Missing Values": missing_total,
            "Original Duplicates": int(source.duplicated().sum()),
            "Records After Cleaning": len(clean_frame),
            "Remaining Duplicates": int(clean_frame.duplicated().sum()),
        })

    reports = {
        "dataset_overview.csv": pd.DataFrame(overview_rows),
        "column_profile_report.csv": pd.DataFrame(column_rows),
        "missing_value_report.csv": pd.DataFrame(missing_rows),
        "duplicate_report.csv": pd.DataFrame(duplicate_rows),
        "id_validation_report.csv": pd.DataFrame(id_rows),
        "categorical_profile_report.csv": pd.DataFrame(categorical_rows),
        "numerical_statistics_report.csv": pd.DataFrame(numerical_rows),
        "iqr_outlier_report.csv": pd.DataFrame(outlier_rows),
        "patient_reference_report.csv": pd.DataFrame(patient_reference_rows),
        "relationship_validation_report.csv": pd.DataFrame(relationship_rows),
        "date_validation_report.csv": pd.DataFrame(date_rows),
        "date_range_validation_report.csv": pd.DataFrame(date_range_rows),
        "business_rule_validation_report.csv": pd.DataFrame(business_rule_rows),
        "cleaning_duplicate_report.csv": pd.DataFrame(cleaned_duplicate_rows),
        "cleaned_data_validation_report.csv": pd.DataFrame(cleaned_validation_rows),
        "data_quality_report.csv": pd.DataFrame(quality_rows),
    }
    return cleaned, reports


def save_outputs(cleaned, reports):
    SILVER_PATH.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.mkdir(parents=True, exist_ok=True)

    for name, frame in cleaned.items():
        filename = name.lower().replace(" ", "_") + "_cleaned.csv"
        frame.to_csv(SILVER_PATH / filename, index=False)

    for filename, report in reports.items():
        report.to_csv(REPORT_PATH / filename, index=False)

    if plt is not None:
        PLOT_PATH.mkdir(parents=True, exist_ok=True)
        missing = reports["missing_value_report.csv"]
        if not missing.empty:
            summary = missing.groupby("Dataset")["Total Missing"].sum().sort_values()
            plt.figure(figsize=(12, 7))
            summary.plot(kind="barh")
            plt.title("Missing Values by Dataset")
            plt.xlabel("Missing Cells")
            plt.ylabel("Dataset")
            plt.tight_layout()
            plt.savefig(PLOT_PATH / "01_missing_values_by_dataset.png", dpi=150)
            plt.close()

        patients = cleaned.get("Patients")
        if patients is not None:
            for column, filename, title in [
                ("GENDER", "02_patient_gender_distribution.png", "Patient Gender Distribution"),
                ("RACE", "03_patient_race_distribution.png", "Patient Race Distribution"),
                ("ETHNICITY", "04_patient_ethnicity_distribution.png", "Patient Ethnicity Distribution"),
            ]:
                if column in patients.columns:
                    counts = patients[column].fillna("Missing").value_counts().head(20)
                    plt.figure(figsize=(9, 5))
                    counts.plot(kind="bar")
                    plt.title(title)
                    plt.xlabel(column.title())
                    plt.ylabel("Patients")
                    plt.xticks(rotation=45, ha="right")
                    plt.tight_layout()
                    plt.savefig(PLOT_PATH / filename, dpi=150)
                    plt.close()

    print("\nProfiling and cleaning completed.")
    print(f"Source datasets: {DATA_PATH}")
    print(f"Cleaned Silver datasets: {SILVER_PATH}")
    print(f"Reports: {REPORT_PATH}")
    print(f"Visualizations: {PLOT_PATH if plt is not None else 'Skipped (matplotlib not installed)'}")
    print("\nDataset overview:")
    print(reports["dataset_overview.csv"].to_string(index=False))
    print("\nData quality summary:")
    print(reports["data_quality_report.csv"].to_string(index=False))


def main():
    warnings.filterwarnings("ignore", category=UserWarning, message="Could not infer format")
    print(f"Project root: {PROJECT_ROOT}")
    datasets = load_datasets()
    cleaned, reports = make_reports(datasets)
    save_outputs(cleaned, reports)


if __name__ == "__main__":
    main()
