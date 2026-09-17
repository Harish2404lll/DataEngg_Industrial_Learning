# EHDP - DATA PROFILING AND CLEANING
# ============================================================
# 1. IMPORT LIBRARIES
# ============================================================
import pandas as pd
import os
import matplotlib.pyplot as plt

# ============================================================
# 2. SET DATASET AND OUTPUT PATH
# ============================================================
DATA_PATH = r"C:\DE\Project\dataset"
OUTPUT_PATH = r"C:\DE\Project\dataprofiling_output"

os.makedirs(OUTPUT_PATH, exist_ok=True)

PLOT_PATH = os.path.join(OUTPUT_PATH, "visualizations")
os.makedirs(PLOT_PATH, exist_ok=True)

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
# 7. COLUMN PROFILE REPORT
# ============================================================
column_report = []

for name, df in datasets.items():
    for column in df.columns:
        column_report.append({
            "Dataset": name,
            "Column": column,
            "Data Type": str(df[column].dtype),
            "Non-Null Values": df[column].notna().sum(),
            "Null Values": df[column].isna().sum(),
            "Unique Values": df[column].nunique(dropna=True)})

column_report = pd.DataFrame(column_report)

# ============================================================
# 8. MISSING VALUE ANALYSIS
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
# 9. DUPLICATE RECORD ANALYSIS
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
# 10. PRIMARY KEY / IDENTIFIER ANALYSIS
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
# 11. UNIQUE VALUE ANALYSIS
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
# 12. CATEGORICAL PROFILING
# ============================================================
print("\n" + "=" * 70)
print("CATEGORICAL PROFILING")
print("=" * 70)

categorical_report = []
for name, df in datasets.items():
    for column in df.columns:
        if (pd.api.types.is_object_dtype(df[column]) or pd.api.types.is_string_dtype(df[column]) or pd.api.types.is_categorical_dtype(df[column])):
            non_null = df[column].dropna()
            unique_count = non_null.nunique()
            if 0 < unique_count <= 50:
                value_counts = non_null.value_counts()
                mode_value = value_counts.index[0]
                mode_frequency = value_counts.iloc[0]
                mode_percentage = round((mode_frequency / len(non_null)) * 100, 2)
                category_percentages = (value_counts / len(non_null) * 100)
                rare_category_count = (category_percentages < 1).sum()
                categorical_report.append({
                    "Dataset": name,
                    "Column": column,
                    "Unique_Values": unique_count,
                    "Mode": mode_value,
                    "Mode_Frequency": mode_frequency,
                    "Mode_Percentage": mode_percentage,
                    "Rare_Categories_Under_1pct": rare_category_count})

categorical_report = pd.DataFrame(categorical_report)

if not categorical_report.empty:
    print(categorical_report.to_string(index=False))
else:
    print("No suitable categorical columns found.")

# ============================================================
# 13. NUMERICAL STATISTICS
# ============================================================
print("\n" + "=" * 70)
print("NUMERICAL STATISTICS")
print("=" * 70)

numerical_report = []
for name, df in datasets.items():
    numeric_data = df.select_dtypes(include="number")
    if len(numeric_data.columns) > 0:
        print(f"\n{name}:")
        for column in numeric_data.columns:
            series = numeric_data[column].dropna()
            numerical_report.append({
                "Dataset": name,
                "Column": column,
                "Count": series.count(),
                "Mean": series.mean(),
                "Std": series.std(),
                "Minimum": series.min(),
                "25%": series.quantile(0.25),
                "Median": series.median(),
                "75%": series.quantile(0.75),
                "Maximum": series.max()})
        print(numeric_data.describe())
    else:
        print(f"\n{name}: No numerical columns available")

numerical_report = pd.DataFrame(numerical_report)

# ============================================================
# 14. IQR OUTLIER ANALYSIS
# ============================================================
print("\n" + "=" * 70)
print("IQR OUTLIER ANALYSIS")
print("=" * 70)

outlier_report = []
for name, df in datasets.items():
    numeric_data = df.select_dtypes(include="number")
    for column in numeric_data.columns:
        series = numeric_data[column].dropna()
        if len(series) == 0:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1

        lower_bound = q1 - (1.5 * iqr)
        upper_bound = q3 + (1.5 * iqr)

        outlier_count = ((series < lower_bound) | (series > upper_bound)).sum()

        outlier_percentage = round((outlier_count / len(series)) * 100, 2)

        outlier_report.append({
            "Dataset": name,
            "Column": column,
            "Q1": q1,
            "Q3": q3,
            "IQR": iqr,
            "Lower_Bound": lower_bound,
            "Upper_Bound": upper_bound,
            "Outlier_Count": outlier_count,
            "Outlier_Percentage": outlier_percentage})

        if outlier_count > 0:
            print(f"{name} - {column}: "
                f"{outlier_count} outliers ({outlier_percentage}%)")

outlier_report = pd.DataFrame(outlier_report)

# ============================================================
# 15. PATIENT REFERENCE VALIDATION
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
# 16. FOREIGN KEY / RELATIONSHIP VALIDATION
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
# 17. DATE VALIDATION
# ============================================================
print("\n" + "=" * 70)
print("DATE VALIDATION")
print("=" * 70)

date_validation_report = []

if "BIRTHDATE" in patients.columns:
    patient_birthdates = pd.to_datetime(patients["BIRTHDATE"],errors="coerce")
    invalid_birthdates = (patient_birthdates.isnull().sum())
    print("Patients - Invalid/Missing Birthdates:",invalid_birthdates)
    date_validation_report.append({
        "Dataset": "Patients",
        "Date Check": "BIRTHDATE",
        "Invalid Dates": invalid_birthdates})

if ("START" in encounters.columns and "STOP" in encounters.columns):
    encounter_start = pd.to_datetime(encounters["START"],errors="coerce")
    encounter_stop = pd.to_datetime(encounters["STOP"],errors="coerce")
    invalid_date_range = (encounter_stop < encounter_start).sum()
    print("Encounters - Invalid date ranges:",invalid_date_range)
    date_validation_report.append({"Dataset": "Encounters","Date Check": "STOP before START","Invalid Dates": invalid_date_range})

date_validation_report = pd.DataFrame(date_validation_report)

# ============================================================
# 18. CREATE CLEAN COPIES OF ALL DATASETS
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
# 19. HEALTHCARE DATE-RANGE VALIDATION
# ============================================================
print("\n" + "=" * 70)
print("HEALTHCARE DATE-RANGE VALIDATION")
print("=" * 70)

date_range_report = []

for name, df in datasets.items():
    if "START" in df.columns and "STOP" in df.columns:
        start_dates = pd.to_datetime(df["START"],errors="coerce",utc=True)
        stop_dates = pd.to_datetime(df["STOP"], errors="coerce",utc=True)
        invalid_range = (stop_dates.notna() & start_dates.notna() & (stop_dates < start_dates)).sum()
        print(f"{name}: {invalid_range} invalid "
            f"STOP-before-START records")
        date_range_report.append({
            "Dataset": name,
            "Check": "STOP before START",
            "Invalid_Records": invalid_range})

date_range_report = pd.DataFrame(date_range_report)

# ============================================================
# 20. BUSINESS-RULE VALIDATION
# ============================================================
print("\n" + "=" * 70)
print("BUSINESS-RULE VALIDATION")
print("=" * 70)

business_rule_report = []

negative_keywords = ["COST","CLAIM","REVENUE","EXPENSE","CHARGE","COVERED"]
for name, df in datasets.items():
    for column in df.columns:
        column_upper = column.upper()
        if any(keyword in column_upper
            for keyword in negative_keywords):
            numeric_values = pd.to_numeric(df[column],errors="coerce")
            negative_count = (numeric_values < 0).sum()
            business_rule_report.append({
                "Dataset": name,
                "Column": column,
                "Rule": "Value should not be negative",
                "Violations": negative_count})
            if negative_count > 0:
                print(f"{name} - {column}: "
                    f"{negative_count} negative values")
                
for name, df in datasets.items():
    if "BMI" in df.columns:
        bmi_values = pd.to_numeric(df["BMI"], errors="coerce")

        invalid_bmi = ((bmi_values <= 0) | (bmi_values > 100)).sum()

        business_rule_report.append({"Dataset": name,
            "Column": "BMI",
            "Rule": "BMI should be greater than 0 and at most 100",
            "Violations": invalid_bmi})

        if invalid_bmi > 0:
            print(f"{name} - BMI: "
                f"{invalid_bmi} possible invalid values")

business_rule_report = pd.DataFrame(business_rule_report)

# ============================================================
# 21. CLEAN SPACES AND EMPTY STRINGS
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
# 22. REMOVE DUPLICATE RECORDS
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
# 23. CLEAN ID AND REFERENCE COLUMNS
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
# 24. STANDARDIZE PATIENT DEMOGRAPHICS
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
# 25. STANDARDIZE CLINICAL CODES
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
# 26. STANDARDIZE DATE COLUMNS
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
# 27. DATASET-SPECIFIC CLEANING
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
# 28. VALIDATE CLEANED DATA
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
# 29. VALIDATE CLEANED PATIENT DATA
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
# 30. FINAL DATA QUALITY REPORT
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
# 31. VISUALIZATION 1 - MISSING VALUES
# ============================================================
print("\n" + "=" * 70)
print("CREATING VISUALIZATIONS")
print("=" * 70)

missing_by_dataset = (missing_report.groupby("Dataset")["Total Missing"].sum().sort_values(ascending=False))

plt.figure(figsize=(12, 7))
missing_by_dataset.plot(kind="bar")
plt.title("Missing Values by Dataset")
plt.xlabel("Dataset")
plt.ylabel("Number of Missing Values")
plt.xticks(rotation=60, ha="right")
plt.tight_layout()
plt.savefig(os.path.join(PLOT_PATH,"01_missing_values_by_dataset.png"))
plt.close()

# ============================================================
# 32. VISUALIZATION 2 - PATIENT GENDER
# ============================================================
if "GENDER" in patients.columns:
    plt.figure(figsize=(7, 5))
    patients["GENDER"].value_counts(dropna=False).plot(kind="bar")
    plt.title("Patient Gender Distribution")
    plt.xlabel("Gender")
    plt.ylabel("Number of Patients")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_PATH,"02_patient_gender_distribution.png"))
    plt.close()

# ============================================================
# 33. VISUALIZATION 3 - PATIENT RACE
# ============================================================
if "RACE" in patients.columns:
    plt.figure(figsize=(9, 6))
    patients["RACE"].value_counts(dropna=False).plot(kind="bar")
    plt.title("Patient Race Distribution")
    plt.xlabel("Race")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_PATH,"03_patient_race_distribution.png"))
    plt.close()

# ============================================================
# 34. VISUALIZATION 4 - PATIENT ETHNICITY
# ============================================================
if "ETHNICITY" in patients.columns:
    plt.figure(figsize=(8, 5))
    patients["ETHNICITY"].value_counts(dropna=False).plot(kind="bar")
    plt.title("Patient Ethnicity Distribution")
    plt.xlabel("Ethnicity")
    plt.ylabel("Number of Patients")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(PLOT_PATH,"04_patient_ethnicity_distribution.png"))
    plt.close()

# ============================================================
# 35. VISUALIZATION 5 - NUMERICAL DISTRIBUTIONS
# ============================================================
plot_count = 0

for name, df in datasets.items():
    numeric_columns = list(df.select_dtypes(include="number").columns)
    for column in numeric_columns:
        if plot_count >= 10:
            break
        plt.figure(figsize=(8, 5))
        df[column].dropna().plot(kind="hist",bins=30)
        plt.title(f"Distribution of {name} - {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.tight_layout()

        safe_name = (name.lower().replace(" ", "_").replace("-", "_"))
        filename = (f"05_numeric_{plot_count + 1}_"
            f"{safe_name}_{column}.png")
        plt.savefig(os.path.join(PLOT_PATH,filename))
        plt.close()
        plot_count += 1

    if plot_count >= 10:
        break

# ============================================================
# 36. SAVE ALL CLEANED DATASETS
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
# 37. SAVE PROFILING REPORTS
# ============================================================

print("\n" + "=" * 70)
print("SAVING PROFILING REPORTS")
print("=" * 70)

reports = {
    "dataset_overview.csv": overview_report,
    "column_profile_report.csv": column_report,
    "missing_value_report.csv": missing_report,
    "duplicate_report.csv": duplicate_report,
    "id_validation_report.csv": id_report,
    "categorical_profile_report.csv": categorical_report,
    "numerical_statistics_report.csv": numerical_report,
    "iqr_outlier_report.csv": outlier_report,
    "patient_reference_report.csv": patient_reference_report,
    "relationship_validation_report.csv": relationship_report,
    "date_validation_report.csv": date_validation_report,
    "date_range_validation_report.csv": date_range_report,
    "business_rule_validation_report.csv": business_rule_report,
    "cleaning_duplicate_report.csv": clean_duplicate_report,
    "cleaned_data_validation_report.csv": validation_report,
    "data_quality_report.csv": quality_report
}

for filename, report in reports.items():
    report.to_csv(os.path.join(OUTPUT_PATH, filename),index=False)
    print("Saved:", filename)

# ============================================================
# 38. FINAL SUMMARY
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

print("\nGenerated reports:")
for filename in reports:
    print("-", filename)

print("\nGenerated visualizations:")
print(PLOT_PATH)

print("\n" + "=" * 70)
print("END OF DATA PROFILING")
print("=" * 70)