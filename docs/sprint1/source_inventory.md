# Sprint 1 — Source inventory

All source paths below are present in the repository tree under `datasets/`. They are synthetic Synthea data.

| Source file | Format | Business area | Main relationship / key |
|---|---|---|---|
| patients.json | JSON | Patient demographics | Id |
| encounters.csv | CSV | Encounters / visits | Id; references PATIENT, ORGANIZATION, PROVIDER, PAYER |
| conditions.csv | CSV | Diagnoses / conditions | PATIENT, ENCOUNTER |
| observations.csv | CSV | Observations and lab-like measurements | PATIENT, ENCOUNTER |
| medications.json | JSON | Medication events | PATIENT, ENCOUNTER, PAYER |
| procedures.csv | CSV | Procedures | PATIENT, ENCOUNTER |
| allergies.json | JSON | Allergies | PATIENT, ENCOUNTER |
| immunizations.csv | CSV | Immunizations | PATIENT, ENCOUNTER |
| organizations.csv | CSV | Hospitals / organizations | Id |
| payers.json | JSON | Payer / insurance information | Id |
| providers.csv | CSV | Healthcare providers | Id; ORGANIZATION |
| payer_transitions.json | JSON | Patient payer history | PATIENT, PAYER |
| careplans.csv | CSV | Care plans | PATIENT, ENCOUNTER |
| devices.csv | CSV | Medical devices | PATIENT, ENCOUNTER |
| imaging_studies.json | JSON | Imaging studies | PATIENT, ENCOUNTER |

## Ingestion verification still required
The repository contains Pentaho transformations and a job file, but file presence alone does not prove successful execution. The patient transformation currently includes a machine-specific source path (`C:\DE\Project\dataset\patients.json`). Check and update source paths and PostgreSQL connection settings on this machine, then run the job and record:
- row count read and written for each file;
- target staging table name and target schema;
- rejected rows and error messages;
- whether reruns create duplicates or update existing rows.

The repository tree currently has placeholder files under `bronze/staging/`; verify actual staging tables in PostgreSQL before marking Sprint 1 ingestion complete.
