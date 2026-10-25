# EHDP Deployment Checklist

Use this checklist from the repository root. Mark an item complete only
after checking it in your own environment.

## A. Before running

-   [ ] Python is installed and available as `python`.
-   [ ] PostgreSQL service is running and the intended EHDP database
    exists.
-   [ ] `requirements.txt` dependencies are installed in the project's
    virtual environment.
-   [ ] `UC2_DATABASE_URL` is set in the current terminal session.
-   [ ] `UC2_TEST_DATABASE_URL` points to a separate test database if
    database-backed tests are to run.
-   [ ] Credentials are kept out of Git; `.env` is ignored by Git if
    used locally.
-   [ ] The source files under `datasets/` have been reviewed and the
    CSV/JSON ingestion mapping is understood.
-   [ ] The selected SQL files have been reviewed for destructive
    statements and schema assumptions.
-   [ ] Pentaho database connections and `.ktr` paths have been checked
    in Spoon, if Pentaho is being used.

## B. Ingestion and warehouse execution

-   [ ] Ingestion script options were reviewed using `--help`.
-   [ ] Target schema and table naming were confirmed against the
    current database.
-   [ ] Source ingestion completed without unreviewed errors.
-   [ ] Source table row counts were recorded.
-   [ ] Warehouse schema/table creation ran in the correct order.
-   [ ] Dimension and fact loads completed.
-   [ ] A repeat run was tested against a safe test database to check
    for duplicate rows/keys.
-   [ ] Any rejected or invalid records were recorded and explained.

## C. Validation

-   [ ] `python -m pytest tests/ -v` was run from the repository root.
-   [ ] Test outcomes were recorded as passed, failed, or skipped.
-   [ ] Database-backed tests were not counted as passed if they were
    skipped.
-   [ ] The applicable SQL validation script was checked for
    schema/table compatibility before execution.
-   [ ] Final warehouse row counts were queried from the current
    database.
-   [ ] Fact-to-dimension relationships and date-key checks were
    verified.
-   [ ] Missing keys, invalid dates, duplicate keys, and rejected
    records were reviewed.
-   [ ] Actual results were saved in the project's validation
    evidence/report.

## D. Reporting and handover

-   [ ] The Power BI `.pbix` file opens in Power BI Desktop.
-   [ ] Data source settings and credentials were configured locally.
-   [ ] Refresh and key visuals were checked, if the report connects to
    the database.
-   [ ] Deployment instructions reflect the actual commands, schema
    names, and paths used.
-   [ ] No passwords, local absolute paths, or real patient data were
    committed.
-   [ ] Known limitations and any skipped/unverified steps are
    documented.

## Record the run

Fill this in after execution; do not pre-fill with expected values.

-   **Run date/time:**
-   **Git commit:**
-   **Database/server (non-secret identifier only):**
-   **Ingestion result:**
-   **Warehouse row counts evidence location:**
-   **Automated tests:** Passed \_\_\_ / Failed \_\_\_ / Skipped \_\_\_
-   **Relationship/data-quality checks:** Passed \_\_\_ / Failed \_\_\_
-   **Rejected records / warnings:**
-   **Power BI open/refresh result:**
-   **Outstanding issues:**
