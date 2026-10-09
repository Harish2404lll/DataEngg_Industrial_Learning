# Sprint 2 — Data profiling and warehouse implementation

## Source data
Reuse the existing synthetic Synthea files in `datasets/`. The raw files are never overwritten. The profiling script writes cleaned CSV copies to `silver/cleansing/`, profiling reports to `docs/sprint2/data_profiling/reports/`, and plots to `docs/sprint2/data_profiling/visualizations/`.

## Run profiling in VS Code
From the repository root:
```powershell
python -m pip install -r requirements.txt
python python/data_profiling.py
```
Paths are resolved relative to the repository, not a personal `C:\DE\Project\...` folder. Review the generated reports before deciding how to handle missing values. Never invent missing clinical values.

## Warehouse design
Run `sql/EDHP_Star_Schema_SQL.sql` in a development database. It defines dimensions for patient, organization, provider, payer, and date, plus two fact tables: encounter (one row per encounter) and observation (one row per observation). Sample analytics are in `sql/sprint2_reporting_queries.sql`.

## Loading order
1. Load patient, organization, and payer dimensions.
2. Load providers after organizations.
3. Populate the date dimension for all encounter and observation dates.
4. Load encounters after the dimensions.
5. Load observations after patients, dates, and encounters.
Map source columns to the target names in Pentaho Select Values before Table Output. Keep UUIDs and clinical codes as text to preserve identifiers and leading zeros.

## Verification checklist
- [ ] Run the Python profiling script successfully.
- [ ] Inspect all profiling reports and Silver CSVs.
- [ ] Execute the DDL in a development database and confirm tables exist.
- [ ] Configure and run Pentaho dimension/fact loads.
- [ ] Run the reporting queries and inspect results.
- [ ] Compare source, Silver, and warehouse row counts.
- [ ] Save screenshots/logs from successful Pentaho and PostgreSQL runs.
- [ ] Commit only after these checks pass.

## Caveats
Synthea data is synthetic. Profiling highlights potential quality issues but does not prove clinical validity. Review outliers instead of automatically deleting them. Defining the target schema does not mean the warehouse is populated; ETL and row-count checks must succeed first.
