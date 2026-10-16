-- UC2 Sprint 2 | Gold patient dimension
-- Exposes the existing warehouse dimension without reloading or replacing it.
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.dim_patients AS
SELECT * FROM warehouse.dim_patient;
