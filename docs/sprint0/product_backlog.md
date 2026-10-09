# EHDP Product Backlog — through Sprint 2

| ID | Priority | User story / work item | Acceptance criteria | Sprint |
|---|---|---|---|---|
| PB-01 | Must | Document business problem, stakeholders, scope, and constraints | BRD and charter reviewed; scope and assumptions explicit | 0 |
| PB-02 | Must | Document the target architecture and repository layout | Diagram and README agree with the chosen tools and layers | 0 |
| PB-03 | Must | Inventory the Synthea sources and define field meanings | Source inventory and data dictionary are reviewed | 1 |
| PB-04 | Must | Ingest CSV and JSON sources with Pentaho | Job completes; row counts and errors are captured for every source | 1 |
| PB-05 | Must | Land source data in PostgreSQL staging | Staging tables exist and row counts reconcile with source files | 1 |
| PB-06 | Must | Profile missing values, duplicates, identifiers, dates, and relationships | Reports are generated from current source files and reviewed | 2 |
| PB-07 | Must | Produce cleaned Silver-layer datasets without changing raw data | Cleaned CSVs are generated; row counts and transformations are documented | 2 |
| PB-08 | Must | Build an analytical star schema | Dimension/fact DDL executes in a development database; keys and grain documented | 2 |
| PB-09 | Must | Load dimensions and facts using Pentaho | Loads succeed; source-to-target row counts and rejected rows recorded | 2 |
| PB-10 | Must | Provide analytical SQL and data-quality checks | Queries execute and results are reviewed | 2 |
| PB-11 | Should | Document lineage, runbook, and evidence | Source-to-target mappings and execution evidence are committed | 2 |

## Definition of Done
A backlog item is done only when its acceptance criteria have been tested and evidence (logs, query results, screenshots, or review notes) is recorded in the repository.
