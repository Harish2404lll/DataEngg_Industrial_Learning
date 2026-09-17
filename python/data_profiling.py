# EHDP - DATA PROFILING AND CLEANING

# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================
import pandas as pd
import os

# ============================================================
# 2. SET DATASET AND OUTPUT PATH
# ============================================================
DATA_PATH = r"C:\DE\Project\dataset"

OUTPUT_PATH = r"C:\DE\Project\dataprofiling_output"

os.makedirs(OUTPUT_PATH, exist_ok=True)

# ============================================================
# 3. LOAD HEALTHCARE DATASETS
# ============================================================
print("\n" + "=" * 70)
print("LOADING HEALTHCARE DATASETS")
print("=" * 70)

patients = pd.read_json(os.path.join(DATA_PATH, "patients.json"))
encounters = pd.read_csv(os.path.join(DATA_PATH, "encounters.csv"))
conditions = pd.read_csv(os.path.join(DATA_PATH, "conditions.csv"))
observations = pd.read_csv(os.path.join(DATA_PATH, "observations.csv"))
medications = pd.read_json(os.path.join(DATA_PATH, "medications.json"))
procedures = pd.read_csv(os.path.join(DATA_PATH, "procedures.csv"))
allergies = pd.read_json(os.path.join(DATA_PATH, "allergies.json"))
immunizations = pd.read_csv(os.path.join(DATA_PATH, "immunizations.csv"))
organizations = pd.read_csv(os.path.join(DATA_PATH, "organizations.csv"))
payers = pd.read_json(os.path.join(DATA_PATH, "payers.json"))
providers = pd.read_csv(os.path.join(DATA_PATH, "providers.csv"))
payer_transitions = pd.read_json(os.path.join(DATA_PATH, "payer_transitions.json"))
careplans = pd.read_csv(os.path.join(DATA_PATH, "careplans.csv"))
devices = pd.read_csv(os.path.join(DATA_PATH, "devices.csv"))
imaging_studies = pd.read_json(os.path.join(DATA_PATH, "imaging_studies.json"))

print("All 15 datasets loaded successfully.")

# ============================================================
# 4. CREATE DATASET DICTIONARY
# ============================================================
datasets = {"Patients": patients,
    "Encounters": encounters,
    "Conditions": conditions,
    "Observations": observations,
    "Medications": medications,
    "Procedures": procedures,
    "Allergies": allergies,
    "Immunizations": immunizations,
    "Organizations": organizations,
    "Payers": payers,
    "Providers": providers,
    "Payer Transitions": payer_transitions,
    "Careplans": careplans,
    "Devices": devices,
    "Imaging Studies": imaging_studies}

# ============================================================
# 5. DATASET OVERVIEW
# ============================================================
print("\n" + "=" * 70)
print("EHDP - DATA PROFILING")
print("=" * 70)

print("\nDATASET OVERVIEW")
overview_report = []
for name, df in datasets.items():
    records = len(df)
    columns = len(df.columns)
    print(f"{name}: {records} records, {columns} columns")
    overview_report.append({"Dataset": name,"Records": records,"Columns": columns})

overview_report = pd.DataFrame(overview_report)

# ============================================================
# 6. COLUMN NAMES AND DATA TYPES
# ============================================================
print("\n" + "=" * 70)
print("COLUMN NAMES AND DATA TYPES")
print("=" * 70)

for name, df in datasets.items():
    print(f"\n{name}")
    for column in df.columns:
        print(f"  {column} - {df[column].dtype}")

# ============================================================
# 7. MISSING VALUE ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("MISSING VALUE ANALYSIS")
print("=" * 70)

missing_report = []
for name, df in datasets.items():
    for column in df.columns:
        nulls = df[column].isnull().sum()
        empty = (df[column].astype("string").str.strip().eq("").sum())

        total_missing = nulls + empty

        if len(df) > 0:
            percentage = round((total_missing / len(df)) * 100,2)
        else:
            percentage = 0

        missing_report.append({
            "Dataset": name,
            "Column": column,
            "Null Values": nulls,
            "Empty Strings": empty,
            "Total Missing": total_missing,
            "Missing Percentage": percentage})

missing_report = pd.DataFrame(missing_report)
print(missing_report.to_string(index=False))

# ============================================================
# 8. DUPLICATE RECORD ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("DUPLICATE RECORD ANALYSIS")
print("=" * 70)

duplicate_report = []
for name, df in datasets.items():
    duplicates = df.duplicated().sum()
    print(f"{name}: {duplicates} duplicate records")
    duplicate_report.append({"Dataset": name,"Duplicate Records": duplicates})
duplicate_report = pd.DataFrame(duplicate_report)

# ============================================================
# 9. PRIMARY KEY / IDENTIFIER ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("PRIMARY KEY / IDENTIFIER ANALYSIS")
print("=" * 70)

id_report = []
for name, df in datasets.items():
    if "Id" in df.columns:
        missing_ids = df["Id"].isnull().sum()
        duplicate_ids = (df["Id"].duplicated().sum())
        print(f"{name}: "
            f"{missing_ids} missing IDs, "
            f"{duplicate_ids} duplicate IDs")
        id_report.append({
            "Dataset": name,
            "Missing IDs": missing_ids,
            "Duplicate IDs": duplicate_ids})
id_report = pd.DataFrame(id_report)

# ============================================================
# 10. UNIQUE VALUE ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("UNIQUE VALUE ANALYSIS")
print("=" * 70)

if "GENDER" in patients.columns:
    print(patients["GENDER"].value_counts(dropna=False))

if "RACE" in patients.columns:
    print(patients["RACE"].value_counts(dropna=False))

if "ETHNICITY" in patients.columns:
    print(patients["ETHNICITY"].value_counts(dropna=False))

if "MARITAL" in patients.columns:
    print(patients["MARITAL"].value_counts(dropna=False))

# ============================================================
# 11. NUMERICAL STATISTICS
# ============================================================
print("\n" + "=" * 70)
print("NUMERICAL STATISTICS")
print("=" * 70)

for name, df in datasets.items():
    numeric_data = df.select_dtypes(include="number")
    if len(numeric_data.columns) > 0:
        print(f"\n{name}:")
        print(numeric_data.describe())
    else:
        print(f"\n{name}: No numerical columns available")

# ============================================================
# 12. PATIENT REFERENCE VALIDATION
# ============================================================
print("\n" + "=" * 70)
print("PATIENT REFERENCE VALIDATION")
print("=" * 70)

patient_reference_report = []
if "Id" in patients.columns:
    patient_ids = set(patients["Id"].dropna().astype(str).str.strip())
    for name, df in datasets.items():
        if "PATIENT" in df.columns:
            references = (df["PATIENT"].dropna().astype(str).str.strip())
            invalid = (~references.isin(patient_ids)).sum()
            print(f"{name}: "f"{invalid} invalid patient references")
            patient_reference_report.append({"Dataset": name,"Invalid Patient References": invalid})

patient_reference_report = pd.DataFrame(patient_reference_report)

# ============================================================
# 13. FOREIGN KEY / RELATIONSHIP VALIDATION
# ============================================================
print("\n" + "=" * 70)
print("FOREIGN KEY / RELATIONSHIP VALIDATION")
print("=" * 70)

relationship_report = []

if "Id" in encounters.columns:
    encounter_ids = set(encounters["Id"].dropna().astype(str).str.strip())
    for name, df in datasets.items():
        if "ENCOUNTER" in df.columns:
            references = (df["ENCOUNTER"].dropna().astype(str).str.strip())
            invalid = (~references.isin(encounter_ids)).sum()
            print(f"{name}: "
                f"{invalid} invalid encounter references")
            relationship_report.append({
                "Dataset": name,
                "Reference Type": "ENCOUNTER",
                "Invalid References": invalid})

if "Id" in organizations.columns:
    organization_ids = set(organizations["Id"].dropna().astype(str).str.strip())
    for name, df in datasets.items():
        if "ORGANIZATION" in df.columns:
            references = (df["ORGANIZATION"].dropna().astype(str).str.strip())
            invalid = (~references.isin(organization_ids)).sum()
            print(f"{name}: "
                f"{invalid} invalid organization references")
            relationship_report.append({
                "Dataset": name,
                "Reference Type": "ORGANIZATION",
                "Invalid References": invalid})

relationship_report = pd.DataFrame(relationship_report)

# ============================================================
# 14. DATE VALIDATION
# ============================================================
print("\n" + "=" * 70)
print("DATE VALIDATION")
print("=" * 70)

date_report = []

if "BIRTHDATE" in patients.columns:
    patient_birthdates = pd.to_datetime(patients["BIRTHDATE"],errors="coerce")
    invalid_birthdates = (patient_birthdates.isnull().sum())
    print("Patients - Invalid/Missing Birthdates:",invalid_birthdates)
    date_report.append({
        "Dataset": "Patients",
        "Date Check": "BIRTHDATE",
        "Invalid Dates": invalid_birthdates})

if ("START" in encounters.columns and "STOP" in encounters.columns):
    encounter_start = pd.to_datetime(encounters["START"],errors="coerce")
    encounter_stop = pd.to_datetime(encounters["STOP"],errors="coerce")
    invalid_date_range = (encounter_stop < encounter_start).sum()
    print("Encounters - Invalid date ranges:",invalid_date_range)
    date_report.append({"Dataset": "Encounters","Date Check": "STOP before START","Invalid Dates": invalid_date_range})

date_report = pd.DataFrame(date_report)

# ============================================================
# 15. CREATE CLEAN COPIES OF ALL DATASETS
# ============================================================
print("\n" + "=" * 70)
print("CREATING CLEAN DATASETS")
print("=" * 70)

patients_clean = patients.copy()
encounters_clean = encounters.copy()
conditions_clean = conditions.copy()
observations_clean = observations.copy()
medications_clean = medications.copy()
procedures_clean = procedures.copy()
allergies_clean = allergies.copy()
immunizations_clean = immunizations.copy()
organizations_clean = organizations.copy()
payers_clean = payers.copy()
providers_clean = providers.copy()
payer_transitions_clean = payer_transitions.copy()
careplans_clean = careplans.copy()
devices_clean = devices.copy()
imaging_studies_clean = imaging_studies.copy()

clean_datasets = {
    "Patients": patients_clean,
    "Encounters": encounters_clean,
    "Conditions": conditions_clean,
    "Observations": observations_clean,
    "Medications": medications_clean,
    "Procedures": procedures_clean,
    "Allergies": allergies_clean,
    "Immunizations": immunizations_clean,
    "Organizations": organizations_clean,
    "Payers": payers_clean,
    "Providers": providers_clean,
    "Payer Transitions": payer_transitions_clean,
    "Careplans": careplans_clean,
    "Devices": devices_clean,
    "Imaging Studies": imaging_studies_clean}
print("Clean copies created for all 15 datasets.")

# ============================================================
# 16. CLEAN SPACES AND EMPTY STRINGS
# ============================================================
print("\n" + "=" * 70)
print("CLEANING SPACES AND EMPTY STRINGS")
print("=" * 70)

for name, df in clean_datasets.items():
    for column in df.columns:
        if (df[column].dtype == "object" or str(df[column].dtype) == "string"):
            df[column] = (df[column].astype("string").str.strip())
            df[column] = df[column].replace("",pd.NA)
    print(f"{name}: text values cleaned")

# ============================================================
# 17. REMOVE DUPLICATE RECORDS
# ============================================================
print("\n" + "=" * 70)
print("REMOVING DUPLICATE RECORDS")
print("=" * 70)

clean_duplicate_report = []
for name, df in clean_datasets.items():
    before = len(df)
    df.drop_duplicates(inplace=True)
    after = len(df)
    removed = before - after
    print(f"{name}: {removed} duplicate records removed")
    clean_duplicate_report.append({
        "Dataset": name,
        "Records Before": before,
        "Records After": after,
        "Duplicates Removed": removed})
clean_duplicate_report = pd.DataFrame(clean_duplicate_report)

# ============================================================
# 18. CLEAN ID AND REFERENCE COLUMNS
# ============================================================
print("\n" + "=" * 70)
print("CLEANING ID AND REFERENCE COLUMNS")
print("=" * 70)

id_columns = ["Id","PATIENT","ENCOUNTER","ORGANIZATION","PROVIDER","PAYER"]

for name, df in clean_datasets.items():
    for column in id_columns:
        if column in df.columns:
            df[column] = (df[column].astype("string").str.strip())
    print(f"{name}: ID/reference columns checked")

# ============================================================
# 19. STANDARDIZE PATIENT DEMOGRAPHICS
# ============================================================
print("\n" + "=" * 70)
print("STANDARDIZING PATIENT DEMOGRAPHICS")
print("=" * 70)

if "GENDER" in patients_clean.columns:
    patients_clean["GENDER"] = (patients_clean["GENDER"].astype("string").str.strip().str.upper())
    patients_clean["GENDER"] = (patients_clean["GENDER"].replace({"MALE": "M","FEMALE": "F"}))

if "RACE" in patients_clean.columns:
    patients_clean["RACE"] = (patients_clean["RACE"].astype("string").str.strip().str.lower())

if "ETHNICITY" in patients_clean.columns:
    patients_clean["ETHNICITY"] = (patients_clean["ETHNICITY"].astype("string").str.strip().str.lower())

if "MARITAL" in patients_clean.columns:
    patients_clean["MARITAL"] = (patients_clean["MARITAL"].astype("string").str.strip().str.upper())

print("Patient demographics standardized.")

# ============================================================
# 20. STANDARDIZE CLINICAL CODES
# ============================================================
print("\n" + "=" * 70)
print("STANDARDIZING CLINICAL CODES")
print("=" * 70)

code_columns = ["CODE","REASONCODE","BODYSITE_CODE","MODALITY_CODE"]

for name, df in clean_datasets.items():
    cleaned_code_columns = []
    for column in code_columns:
        if column in df.columns:
            df[column] = (df[column].astype("string").str.strip())
            cleaned_code_columns.append(column)

    if len(cleaned_code_columns) > 0:
        print(f"{name}: "
            f"{', '.join(cleaned_code_columns)} cleaned")

# ============================================================
# 21. STANDARDIZE DATE COLUMNS
# ============================================================
print("\n" + "=" * 70)
print("STANDARDIZING DATE COLUMNS")
print("=" * 70)

date_columns = ["BIRTHDATE","START","STOP","DATE"]

for name, df in clean_datasets.items():
    cleaned_date_columns = []
    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(df[column],errors="coerce")
            cleaned_date_columns.append(column)

    if len(cleaned_date_columns) > 0:
        print(f"{name}: "
            f"{', '.join(cleaned_date_columns)} converted")

# ============================================================
# 22. DATASET-SPECIFIC CLEANING
# ============================================================
print("\n" + "=" * 70)
print("DATASET-SPECIFIC CLEANING")
print("=" * 70)

if "PATIENT" in payer_transitions_clean.columns:
    payer_transitions_clean["PATIENT"] = (payer_transitions_clean["PATIENT"].astype("string").str.strip())

if "PAYER" in payer_transitions_clean.columns:
    payer_transitions_clean["PAYER"] = (payer_transitions_clean["PAYER"].astype("string").str.strip())

if "BODYSITE_CODE" in imaging_studies_clean.columns:
    imaging_studies_clean["BODYSITE_CODE"] = (imaging_studies_clean["BODYSITE_CODE"].astype("string").str.strip())

if "MODALITY_CODE" in imaging_studies_clean.columns:
    imaging_studies_clean["MODALITY_CODE"] = (imaging_studies_clean["MODALITY_CODE"].astype("string").str.strip())

print("Dataset-specific cleaning completed.")

# ============================================================
# 23. VALIDATE CLEANED DATA
# ============================================================
print("\n" + "=" * 70)
print("VALIDATING CLEANED DATA")
print("=" * 70)

validation_report = []
for name, df in clean_datasets.items():
    duplicates = df.duplicated().sum()
    if "Id" in df.columns:
        missing_ids = df["Id"].isnull().sum()
    else:
        missing_ids = "N/A"

    validation_report.append({
        "Dataset": name,
        "Records": len(df),
        "Remaining Duplicates": duplicates,
        "Missing IDs": missing_ids})

    print(f"{name}: "
        f"{len(df)} records, "
        f"{duplicates} remaining duplicates")

validation_report = pd.DataFrame(validation_report)

# ============================================================
# 24. VALIDATE CLEANED PATIENT DATA
# ============================================================
print("\n" + "-" * 70)
print("PATIENT DATA VALIDATION")
print("-" * 70)

if "Id" in patients_clean.columns:
    print("Missing Patient IDs:",patients_clean["Id"].isnull().sum())
    print("Duplicate Patient IDs:",patients_clean["Id"].duplicated().sum())

if "GENDER" in patients_clean.columns:
    print("\nCleaned Gender Values:")
    print(patients_clean["GENDER"].value_counts(dropna=False))

if "RACE" in patients_clean.columns:
    print("\nCleaned Race Values:")
    print(patients_clean["RACE"].value_counts(dropna=False))

if "ETHNICITY" in patients_clean.columns:
    print("\nCleaned Ethnicity Values:")
    print(patients_clean["ETHNICITY"].value_counts(dropna=False))

if "MARITAL" in patients_clean.columns:
    print("\nCleaned Marital Status Values:")
    print(patients_clean["MARITAL"].value_counts(dropna=False))

# ============================================================
# 25. CREATE FINAL DATA QUALITY REPORT
# ============================================================
print("\n" + "=" * 70)
print("FINAL DATA QUALITY REPORT")
print("=" * 70)

quality_report = []
for name, df in datasets.items():
    total_missing = (missing_report.loc[missing_report["Dataset"] == name,"Total Missing"].sum())
    original_duplicates = (df.duplicated().sum())
    clean_df = clean_datasets[name]
    remaining_duplicates = (clean_df.duplicated().sum())
    quality_report.append({
        "Dataset": name,
        "Original Records": len(df),
        "Columns": len(df.columns),
        "Missing Values": total_missing,
        "Original Duplicates": original_duplicates,
        "Records After Cleaning": len(clean_df),
        "Remaining Duplicates": remaining_duplicates})
quality_report = pd.DataFrame(quality_report)
print(quality_report.to_string(index=False))

# ============================================================
# 26. SAVE ALL CLEANED DATASETS
# ============================================================
print("\n" + "=" * 70)
print("SAVING CLEANED DATASETS")
print("=" * 70)

for name, df in clean_datasets.items():
    filename = (name.lower().replace(" ", "_")+ "_cleaned.csv")
    file_path = os.path.join(OUTPUT_PATH,filename)
    df.to_csv(file_path,index=False)
    print("Saved:",filename)

# ============================================================
# 27. SAVE PROFILING REPORTS
# ============================================================
print("\n" + "=" * 70)
print("SAVING PROFILING REPORTS")
print("=" * 70)

overview_report.to_csv(os.path.join(OUTPUT_PATH,"dataset_overview.csv"),index=False)
missing_report.to_csv(os.path.join(OUTPUT_PATH,"missing_value_report.csv"),index=False)
duplicate_report.to_csv(os.path.join(OUTPUT_PATH,"duplicate_report.csv"),index=False)
id_report.to_csv(os.path.join(OUTPUT_PATH,"id_validation_report.csv"),index=False)
patient_reference_report.to_csv(os.path.join(OUTPUT_PATH,"patient_reference_report.csv"),index=False)
relationship_report.to_csv(os.path.join(OUTPUT_PATH,"relationship_validation_report.csv"),index=False)
date_report.to_csv(os.path.join(OUTPUT_PATH,"date_validation_report.csv"),index=False)
clean_duplicate_report.to_csv(os.path.join(OUTPUT_PATH,"cleaning_duplicate_report.csv"),index=False)
quality_report.to_csv(os.path.join(OUTPUT_PATH,"data_quality_report.csv"),index=False)
validation_report.to_csv(os.path.join(OUTPUT_PATH,"cleaned_data_validation_report.csv"),index=False)

# ============================================================
# 28. FINAL MESSAGE
# ============================================================
print("\n" + "=" * 70)
print("EHDP DATA PROFILING COMPLETED SUCCESSFULLY")
print("=" * 70)

print("\nOutput folder:")
print(OUTPUT_PATH)
print("\nCleaned datasets and reports have been saved.")

print("\nCleaned datasets:")
for name in clean_datasets.keys():
    filename = (name.lower().replace(" ", "_")+ "_cleaned.csv")
    print("-", filename)

print("\nReports:")
print("- dataset_overview.csv")
print("- missing_value_report.csv")
print("- duplicate_report.csv")
print("- id_validation_report.csv")
print("- patient_reference_report.csv")
print("- relationship_validation_report.csv")
print("- date_validation_report.csv")
print("- cleaning_duplicate_report.csv")
print("- data_quality_report.csv")
print("- cleaned_data_validation_report.csv")

print("\n" + "=" * 70)
print("END OF DATA PROFILING")
print("=" * 70)