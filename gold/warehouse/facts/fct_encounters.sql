-- UC2 Sprint 2 | Existing encounter fact table exposed to Gold consumers
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.fct_encounters AS
SELECT * FROM warehouse.fact_encounter;
