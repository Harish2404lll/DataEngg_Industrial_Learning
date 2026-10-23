# Enterprise Healthcare Data Platform (EHDP)

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![Database](https://img.shields.io/badge/Database-PostgreSQL-336791)](https://www.postgresql.org/)
[![ETL](https://img.shields.io/badge/ETL-Pentaho-4B8BBE)](https://www.hitachivantara.com/en-us/products/data-management-analytics/pentaho.html)
[![Status](https://img.shields.io/badge/Project-Sprints%200%E2%80%933%20Completed-success)](#sprint-deliverables)

EHDP is a healthcare data engineering project that brings synthetic clinical and hospital data into a structured platform for data quality, warehousing, metadata management, and analytics.

> **Data privacy:** The project uses synthetic healthcare data from [Synthea](https://synthetichealth.github.io/synthea/), not real patient records.

## Table of contents

- [Project goals](#project-goals)
- [Architecture](#architecture)
- [Sprint deliverables](#sprint-deliverables)
- [Technology stack](#technology-stack)
- [Repository guide](#repository-guide)
- [Getting started](#getting-started)
- [Running tests](#running-tests)
- [Reports and documentation](#reports-and-documentation)

## Project goals

- Ingest healthcare source data supplied as CSV and JSON.
- Keep ingestion separate from downstream cleansing and validation.
- Profile datasets and document data-quality findings.
- Design and load relational warehouse structures for analysis.
- Create analytical dimensions, facts, and data marts.
- Document table/column metadata, lineage, and validation evidence.
- Keep code and project artifacts version-controlled and testable.

## Architecture

```text
                 Synthea source datasets
                       CSV / JSON
                          |
                          v
                 +------------------+
                 | Bronze / Ingest  |
                 | Raw source data  |
                 +------------------+
                          |
                          v
                 +------------------+
                 | Silver / Quality |
                 | Profiling, rules,|
                 | cleansing checks |
                 +------------------+
                          |
                          v
                 +------------------+
                 | Warehouse / Gold |
                 | Dimensions, facts|
                 | and data marts   |
                 +------------------+
                          |
                          v
                 Reporting and analytics
```

The repository includes Python ingestion and profiling utilities, PostgreSQL SQL scripts, Pentaho jobs and transformations, a Power BI star-schema artifact, data-quality reports, metadata SQL, lineage documentation, and tests.

## Sprint deliverables

All project work across **Sprint 0, Sprint 1, Sprint 2, and Sprint 3 is completed**.

| Sprint | Focus | Key deliverables |
|---|---|---|
| **Sprint 0** | Planning and architecture | Project charter, business requirements, architecture diagram |
| **Sprint 1** | Source data and ingestion | Synthea datasets, CSV/JSON ingestion scripts, Pentaho ingestion job and transformations, data dictionary |
| **Sprint 2** | Profiling and warehouse modeling | Data-quality reports, cleaned datasets, star schema, warehouse SQL, ETL job, Power BI artifact |
| **Sprint 3** | Metadata and analytical layer | Metadata repository SQL, Gold dimensions and facts, analytical data marts, validation report |

### Sprint 0 — Planning and architecture

- [Project charter](docs/sprint0/UC2_Project_Charter.pdf)
- [Business requirements](docs/sprint0/Business%20Requirement%20Document.docx)
- [Architecture diagram](docs/sprint0/Architecture_Diagram.png)

### Sprint 1 — Source data and ingestion

- Source datasets are in [`datasets/`](datasets/).
- CSV and JSON PostgreSQL ingestion scripts are in [`bronze/ingestion/`](bronze/ingestion/).
- Pentaho jobs and transformations are in [`pentaho/`](pentaho/).
- [Sprint 1 data dictionary](docs/sprint1/data_dictionary.xlsx)

### Sprint 2 — Data quality and warehouse modeling

- Profiling utility: [`python/data_profiling.py`](python/data_profiling.py)
- Profiling and cleansing outputs: [`docs/sprint2/data_profiling/reports/`](docs/sprint2/data_profiling/reports/)
- Star-schema SQL: [`docs/sprint2/star_schema/EDHP_Star_Schema_SQL.sql`](docs/sprint2/star_schema/EDHP_Star_Schema_SQL.sql)
- Warehouse creation, loading, and validation scripts: [`sql/`](sql/)
- Pentaho job: [`pentaho/jobs/EDHP_Sprint2.kjb`](pentaho/jobs/EDHP_Sprint2.kjb)
- Power BI star-schema artifact: [`docs/sprint2/star_schema/EHDP%20Star%20Schema.pbix`](docs/sprint2/star_schema/EHDP%20Star%20Schema.pbix)

### Sprint 3 — Metadata and analytical layer

- [Metadata repository SQL](docs/sprint3/metadata_repository.sql)
- [Sprint 3 validation report](docs/sprint3/validation_report.xlsx)
- Gold dimensions: [`gold/dimensions/`](gold/dimensions/)
- Gold facts: [`gold/facts/`](gold/facts/)
- Analytical data marts: [`gold/marts/`](gold/marts/)
- Data lineage documents: [`lineage/`](lineage/)

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Ingestion utilities, profiling, and test support |
| Pandas and NumPy | Tabular data processing and analysis |
| PostgreSQL | Relational storage and warehouse SQL |
| SQLAlchemy and psycopg2 | Python-to-PostgreSQL connectivity |
| Pentaho Data Integration | ETL jobs and transformations |
| Power BI | Star-schema/reporting artifact |
| pytest | Automated tests |
| Git and GitHub Actions | Version control and CI workflow |

## Repository guide

```text
.
├── datasets/                    # Synthetic healthcare CSV and JSON data
├── bronze/
│   ├── ingestion/                # CSV and JSON ingestion scripts
│   └── staging/                  # Staging schema SQL
├── silver/cleansing/             # Data-quality and profiling reports
├── gold/
│   ├── dimensions/               # Dimension SQL
│   ├── facts/                    # Fact SQL
│   └── marts/                    # Analytical data marts
├── sql/                          # Warehouse creation, load, and validation SQL
├── python/                       # Profiling utilities
├── pentaho/
│   ├── jobs/                     # Pentaho jobs
│   └── transformations/          # Pentaho transformations
├── metadata/                     # Data dictionary and metadata artifacts
├── lineage/                      # Data lineage documentation
├── docs/
│   ├── sprint0/                  # Charter, requirements, architecture
│   ├── sprint1/                  # Data dictionary
│   ├── sprint2/                  # Profiling, reports, star schema
│   └── sprint3/                  # Metadata SQL and validation report
├── tests/                        # Automated tests
├── .github/workflows/            # GitHub Actions workflows
└── requirements.txt              # Python dependencies
```

## Getting started

### Prerequisites

- Python installed and available as `python` (or `python3`).
- PostgreSQL for database-backed ingestion and SQL workflows.
- Pentaho Data Integration if you want to run the supplied `.kjb` and `.ktr` files.
- Power BI Desktop to open the supplied `.pbix` artifact.

### 1. Clone the repository

```bash
git clone https://github.com/Harish2404lll/DataEngg_Industrial_Learning.git
cd DataEngg_Industrial_Learning
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure the database connection

Set the connection string for the ingestion scripts in your terminal session. For Windows PowerShell:

```powershell
$env:UC2_DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@localhost:5432/uc2"
```

Replace the example username, password, host, and database with your own PostgreSQL configuration. Do not commit credentials to the repository.

### 5. Review ingestion options before running

The scripts support command-line options for the source directory, target schema, and table behavior. Check the current options first:

```bash
python bronze/ingestion/ingest_csv_sources.py --help
python bronze/ingestion/ingest_json_sources.py --help
```

The committed source files are mixed CSV and JSON formats in `datasets/`. Choose the appropriate script for each format and confirm its table naming/mapping and destination schema match your database setup before ingestion. The scripts default to the `bronze` schema; database tests may expect a separately prepared test database and table names. Do not assume ingestion alone creates every warehouse or Gold object.

### 6. Execute the warehouse and ETL artifacts

Review the SQL files in `sql/` and the jobs/transformation files in `pentaho/`. Configure database connections, source and target schemas, and the execution order for your environment before running the complete workflow. The repository includes SQL for warehouse table creation, dimension/fact loading, validation, and metadata repository setup.

## Running tests

Run the Python test suite from the repository root:

```bash
python -m pytest tests/ -v
```

Some database-backed tests are skipped unless `UC2_TEST_DATABASE_URL` is configured. Point this variable to a suitable test database whose schema and expected tables are prepared for the checks. A test run is not evidence of database validation unless the database-backed tests actually execute.

The GitHub Actions workflow is located in [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

## Reports and documentation

| Artifact | Location |
|---|---|
| Data dictionary | [`metadata/data_dictionary.xlsx`](metadata/data_dictionary.xlsx) |
| Profiling reports and cleaned data | [`docs/sprint2/data_profiling/reports/`](docs/sprint2/data_profiling/reports/) |
| Data-quality report | [`silver/cleansing/data_quality_report.csv`](silver/cleansing/data_quality_report.csv) |
| Star-schema SQL | [`docs/sprint2/star_schema/EDHP_Star_Schema_SQL.sql`](docs/sprint2/star_schema/EDHP_Star_Schema_SQL.sql) |
| Warehouse validation SQL | [`sql/04_validate_warehouse.sql`](sql/04_validate_warehouse.sql) |
| Final Sprint 2 validation SQL | [`sql/05_sprint2_final_validation.sql`](sql/05_sprint2_final_validation.sql) |
| Metadata repository SQL | [`docs/sprint3/metadata_repository.sql`](docs/sprint3/metadata_repository.sql) |
| Sprint 3 validation report | [`docs/sprint3/validation_report.xlsx`](docs/sprint3/validation_report.xlsx) |
| Data lineage documentation | [`lineage/`](lineage/) |

## Notes

- The project data is synthetic; it should not be interpreted as real clinical data.
- Run ingestion and SQL operations in a development/test database before using another environment.
- Source paths, connection details, schema names, and table mappings can vary by local setup.
- Validation reports are stored project artifacts; rerun relevant checks after changing data or transformation logic.

## Repository

[Open the EHDP GitHub repository](https://github.com/Harish2404lll/DataEngg_Industrial_Learning)
