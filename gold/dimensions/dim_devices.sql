-- UC2 Sprint 2 | Distinct device descriptors
-- Synthea device rows do not contain a dedicated device_id.
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.dim_devices AS
SELECT DISTINCT code AS device_code, description, udi
FROM public.uc2_devices;
