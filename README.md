# Enterprise Healthcare Data Platform (EHDP)

An enterprise healthcare data engineering project that integrates synthetic healthcare datasets, performs data profiling and cleansing, builds a PostgreSQL data warehouse, and prepares data for analytics.

**Data Source:** [Synthea](https://synthetichealth.github.io/synthea/) – synthetic healthcare data; no real patient records are used.

## Project Objectives

- Ingest healthcare data from CSV and JSON sources.
- Profile, clean, and validate datasets using Python.
- Store and manage data using PostgreSQL.
- Build a dimensional data warehouse using a Star Schema.
- Develop ETL pipelines using Pentaho.
- Maintain metadata, data quality, and data lineage.
- Prepare analytics-ready datasets.

## Architecture

```text
Synthea Datasets
       |
       v
Bronze - Raw Data Ingestion
       |
       v
Silver - Profiling, Cleansing
         and Validation
       |
       v
Gold - Dimensions, Facts
       and Data Marts
       |
       v
Reporting and Analytics
```

## Sprint Deliverables

| Sprint | Focus | Key Deliverables |
|---|---|---|
| Sprint 0 | Project Planning | Project Charter, BRD, Architecture |
| Sprint 1 | Data Ingestion | Source Inventory, Data Dictionary, Pentaho Pipelines |
| Sprint 2 | Profiling and Warehousing | Profiling Reports, Data Quality Reports, Star Schema, PostgreSQL Warehouse |
| Sprint 3 | Governance and Analytics | Metadata, Data Lineage, Data Marts, Validation |

## Technology Stack

- **ETL:** Pentaho Data Integration
- **Database:** PostgreSQL
- **Programming:** Python, Pandas, NumPy
- **Version Control:** Git and GitHub
- **Reporting:** Power BI
- **Testing:** pytest

## Repository Structure

```text
├── datasets/
├── bronze/
│   ├── ingestion/
│   └── staging/
├── silver/
│   ├── cleansing/
│   ├── validation/
│   └── transformations/
├── gold/
│   ├── dimensions/
│   ├── facts/
│   └── marts/
├── pentaho/
│   ├── jobs/
│   └── transformations/
├── python/
├── sql/
├── metadata/
├── lineage/
├── docs/
├── tests/
├── requirements.txt
└── README.md
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/febisarju/DataEngg_Industrial_Learning.git
cd DataEngg_Industrial_Learning
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Set your database connection string:

```powershell
$env:UC2_DATABASE_URL = "postgresql+psycopg2://USER:PASSWORD@localhost:5432/uc2"
```

Replace the example credentials with your own. Do not commit database credentials.

### 5. Run tests

```bash
python -m pytest tests/ -v
```

Review the SQL scripts and Pentaho jobs before executing them. Configure the database connections, schemas, and source paths for your environment.

## Documentation and Reports

- **Sprint 0:** `docs/sprint0/`
- **Sprint 1:** `docs/sprint1/`
- **Sprint 2:** `docs/sprint2/`
- **Sprint 3:** `docs/sprint3/`
- **SQL Scripts:** `sql/`
- **Data Quality:** `silver/cleansing/`
- **Metadata:** `metadata/`
- **Data Lineage:** `lineage/`

## Notes

- The project uses synthetic healthcare data for educational purposes.
- Database connection details and local file paths must be configured before execution.
- Run database operations in a development environment.

**Repository:** [DataEngg_Industrial_Learning](https://github.com/febisarju/DataEngg_Industrial_Learning)
