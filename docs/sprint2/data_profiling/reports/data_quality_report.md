# Sprint 2 – Data Quality Assessment Report

## 1. Introduction

As part of Sprint 2 of the Enterprise Healthcare Data Platform (EHDP) project, data profiling and quality checks were performed on 15 Synthea healthcare datasets. The purpose was to understand the structure of the data, identify missing values and duplicate records, validate date sequences, and prepare the datasets for further processing and data warehouse integration.

The profiling process generated dataset overview reports, missing-value reports, duplicate-cleaning reports, date-validation reports, and other profiling outputs. These reports were used to identify potential data-quality issues and decide how they should be handled.

## 2. Dataset Overview

The profiling process covered the following 15 datasets.

| Dataset | Records | Columns |
|---|---:|---:|
| Patients | 1,171 | 25 |
| Encounters | 53,346 | 15 |
| Conditions | 8,376 | 6 |
| Observations | 299,697 | 8 |
| Medications | 42,989 | 13 |
| Procedures | 34,981 | 8 |
| Allergies | 597 | 6 |
| Immunizations | 15,478 | 6 |
| Organizations | 1,119 | 11 |
| Payers | 10 | 21 |
| Providers | 5,855 | 12 |
| Payer Transitions | 3,801 | 5 |
| Careplans | 3,483 | 9 |
| Devices | 78 | 7 |
| Imaging Studies | 855 | 10 |

The Observations dataset contains the largest number of records, while the Payers dataset contains the fewest. These datasets represent different aspects of patient demographics, healthcare encounters, clinical observations, medications, procedures, and healthcare organizations.

## 3. Missing Values and Their Handling

The missing-value report identified incomplete fields across several datasets. Missing values were assessed according to the meaning of each field rather than automatically treating every missing value as an error.

### 3.1 Important Missing-Value Findings

| Dataset | Column | Missing Values | Missing Percentage |
|---|---|---:|---:|
| Patients | DEATHDATE | 1,000 | 85.40% |
| Patients | ZIP | 543 | 46.37% |
| Encounters | REASONCODE | 39,569 | 74.17% |
| Encounters | REASONDESCRIPTION | 39,569 | 74.17% |
| Conditions | STOP | 3,811 | 45.50% |
| Observations | ENCOUNTER | 30,363 | 10.13% |
| Observations | UNITS | 12,735 | 4.25% |
| Medications | STOP | 1,895 | 4.41% |
| Medications | REASONCODE | 11,117 | 25.86% |
| Medications | REASONDESCRIPTION | 11,117 | 25.86% |
| Procedures | REASONCODE | 15,544 | 44.44% |
| Procedures | REASONDESCRIPTION | 15,544 | 44.44% |
| Allergies | STOP | 533 | 89.28% |
| Organizations | PHONE | 184 | 16.44% |
| Payers | ADDRESS, CITY, STATE_HEADQUARTERED, ZIP, PHONE | 1 each | 10.00% each |
| Payer Transitions | OWNERSHIP | 236 | 6.21% |
| Careplans | STOP | 1,532 | 43.99% |
| Careplans | REASONCODE | 327 | 9.39% |
| Careplans | REASONDESCRIPTION | 327 | 9.39% |
| Devices | STOP | 78 | 100.00% |

### 3.2 Handling Decisions

Missing values were considered in the context of the relevant healthcare information.

- **Patient death dates:** Missing DEATHDATE values were retained because a missing death date may indicate that the patient is alive or that no death date has been recorded.
- **Missing ZIP codes and phone numbers:** These were documented rather than replaced with invented information.
- **Missing clinical reasons:** Missing REASONCODE and REASONDESCRIPTION values may indicate that no reason was recorded for an encounter, medication, procedure, or care plan.
- **Missing STOP dates:** Missing end dates in conditions, medications, allergies, and care plans may represent records with no recorded end date. They should not automatically be classified as invalid.
- **Missing observation references and units:** Missing ENCOUNTER values require relationship validation. Missing UNITS values should be reviewed according to the type of observation.
- **Missing payer-transition ownership:** Missing OWNERSHIP values require review to determine whether the information is available from a reliable source.

No missing clinical information should be fabricated. Where a missing value is legitimate, the record should be retained. Where it affects an important relationship or calculation, it should be flagged for investigation.

The missing-value report identifies the affected fields and their counts. It does not, by itself, prove that every missing value was filled or corrected.

## 4. Duplicate Records Detected and Removed

Duplicate records were assessed across all 15 datasets. The duplicate-cleaning report shows that duplicate removal affected only the Observations dataset.

| Dataset | Records Before | Records After | Duplicates Removed |
|---|---:|---:|---:|
| Patients | 1,171 | 1,171 | 0 |
| Encounters | 53,346 | 53,346 | 0 |
| Conditions | 8,376 | 8,376 | 0 |
| Observations | 299,697 | 299,255 | 442 |
| Medications | 42,989 | 42,989 | 0 |
| Procedures | 34,981 | 34,981 | 0 |
| Allergies | 597 | 597 | 0 |
| Immunizations | 15,478 | 15,478 | 0 |
| Organizations | 1,119 | 1,119 | 0 |
| Payers | 10 | 10 | 0 |
| Providers | 5,855 | 5,855 | 0 |
| Payer Transitions | 3,801 | 3,801 | 0 |
| Careplans | 3,483 | 3,483 | 0 |
| Devices | 78 | 78 | 0 |
| Imaging Studies | 855 | 855 | 0 |

The Observations dataset originally contained 299,697 records. A total of 442 duplicate records were removed, leaving 299,255 records.

The number of records removed represents approximately 0.15% of the original Observations dataset.

The record counts of the other 14 datasets remained unchanged during duplicate cleaning. The original source data should be retained so that the cleaning process can be reviewed and reproduced.

## 5. Invalid Dates and Date Validation

Date validation was performed to identify invalid dates and incorrect chronological sequences.

The date-range validation report produced the following results.

| Dataset | Validation Check | Invalid Records |
|---|---|---:|
| Encounters | STOP before START | 0 |
| Conditions | STOP before START | 0 |
| Medications | STOP before START | 5 |
| Allergies | STOP before START | 0 |
| Careplans | STOP before START | 0 |
| Devices | STOP before START | 0 |

The date-validation report also identified zero invalid BIRTHDATE values in the Patients dataset and zero invalid date sequences for the Encounters check shown in that report.

Five medication records were flagged because their STOP dates occurred before their START dates. This is an invalid chronological sequence and requires investigation.

The five records should not be described as corrected or removed unless the cleaning script confirms that action. The appropriate handling is to verify the source values and correct them only when reliable information is available. Otherwise, they should be flagged or handled according to the project's data-quality rules.

The reported results apply to the checks listed above and should not be interpreted as confirmation that every date field in all 15 datasets was validated.

## 6. Records Intentionally Retained

Some records were retained because missing values may be legitimate in the healthcare context.

### 6.1 Devices Dataset

The Devices dataset contains 78 records, and all 78 have missing STOP dates.

A missing STOP date does not necessarily indicate an invalid device record. It may mean that the device is still in use or that an end date has not been recorded.

Therefore, these records should not automatically be deleted. They should be retained when consistent with the project's business rules, and the missing end dates should be documented for further review.

### 6.2 Other Clinical Records

Missing end dates in conditions, medications, allergies, and care plans may also be valid when no end date has been recorded. Similarly, missing reason fields may be legitimate when the reason for a clinical event was not documented.

These records should be evaluated according to their meaning and intended use rather than removed solely because a field is missing.

## 7. Standardization and Data Preparation

Data preparation is necessary to make the healthcare datasets suitable for downstream processing and warehouse integration.

The profiling outputs include column profiles, categorical profiles, numerical statistics, date-validation reports, identifier-validation reports, and cleaned dataset files.

The following checks are relevant to the preparation process:

- Verify that date fields have appropriate and consistent data types.
- Check that numeric fields contain valid numeric values.
- Preserve patient, encounter, provider, organization, and other identifiers in a form that does not alter their values.
- Review missing-value representations and inconsistent data types.
- Validate patient and encounter references before warehouse loading.
- Document any values that were standardized or corrected.

The generated reports help identify areas requiring attention. Specific standardization operations should be recorded as completed only when confirmed by the Python script and its outputs.

## 8. Summary of Data-Quality Findings

| Quality Check | Finding | Status |
|---|---|---|
| Missing values | Identified across multiple datasets | Assessed and documented |
| Duplicate records | 442 duplicate observations removed | Confirmed by duplicate report |
| Medication date order | 5 records flagged | Requires review of final treatment |
| Patient birth dates | 0 invalid values reported | Confirmed for the reported check |
| Other date-range checks | 0 invalid records in the listed checks, except Medications | Confirmed for the reported checks |
| Device STOP dates | 78 missing values out of 78 records | Retained for context-aware review |
| Standardization | Profiling and preparation outputs generated | Specific transformations require code verification |

## 9. Conclusion

Data profiling was performed on 15 Synthea healthcare datasets as part of Sprint 2 of the EHDP project. The process identified missing values, duplicate records, and date-related inconsistencies that could affect downstream data processing.

The duplicate-cleaning report confirmed that 442 duplicate records were removed from the Observations dataset, reducing its record count from 299,697 to 299,255. Date validation identified five medication records with STOP dates earlier than START dates. The remaining date-range checks listed in the report showed no invalid records.

Missing values were assessed according to the meaning of each field. In particular, missing device STOP dates were not automatically treated as errors because they may represent ongoing device use. Other missing values require appropriate handling based on whether the information is optional, unavailable, or necessary for reliable analysis.

These profiling results provide a basis for documenting data-quality issues and preparing the datasets for subsequent integration into the EHDP data warehouse. Before warehouse loading is considered complete, the flagged medication records, required relationships, and actual standardization operations should be verified, and the profiling reports should be checked for correct column labels and calculations.