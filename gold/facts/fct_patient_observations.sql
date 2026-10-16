-- UC2 Sprint 2 | Existing observation fact table exposed to Gold consumers
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.fct_patient_observations AS
SELECT * FROM warehouse.fact_observation;
