
-- EHDP Sprint 2: final validation evidence
-- Read-only checks; does not modify warehouse data.

-- 1. Warehouse row counts
SELECT 'dim_date' AS table_name, COUNT(*) AS row_count
FROM warehouse.dim_date
UNION ALL
SELECT 'dim_patient', COUNT(*) FROM warehouse.dim_patient
UNION ALL
SELECT 'dim_organization', COUNT(*) FROM warehouse.dim_organization
UNION ALL
SELECT 'dim_provider', COUNT(*) FROM warehouse.dim_provider
UNION ALL
SELECT 'dim_payer', COUNT(*) FROM warehouse.dim_payer
UNION ALL
SELECT 'fact_encounter', COUNT(*) FROM warehouse.fact_encounter
UNION ALL
SELECT 'fact_observation', COUNT(*) FROM warehouse.fact_observation
ORDER BY table_name;

-- 2. Encounter relationship validation
SELECT
    'Encounter: missing patient' AS check_name,
    COUNT(*) AS failed_records
FROM warehouse.fact_encounter f
LEFT JOIN warehouse.dim_patient p
    ON f.patient_key = p.patient_key
WHERE p.patient_key IS NULL

UNION ALL

SELECT 'Encounter: missing organization', COUNT(*)
FROM warehouse.fact_encounter f
LEFT JOIN warehouse.dim_organization o
    ON f.organization_key = o.organization_key
WHERE f.organization_key IS NOT NULL
  AND o.organization_key IS NULL

UNION ALL

SELECT 'Encounter: missing provider', COUNT(*)
FROM warehouse.fact_encounter f
LEFT JOIN warehouse.dim_provider p
    ON f.provider_key = p.provider_key
WHERE f.provider_key IS NOT NULL
  AND p.provider_key IS NULL

UNION ALL

SELECT 'Encounter: missing payer', COUNT(*)
FROM warehouse.fact_encounter f
LEFT JOIN warehouse.dim_payer p
    ON f.payer_key = p.payer_key
WHERE f.payer_key IS NOT NULL
  AND p.payer_key IS NULL;

-- 3. Observation source-data limitation
SELECT
    COUNT(*) AS total_observations,
    COUNT(*) FILTER (
        WHERE encounter_key IS NULL
    ) AS missing_encounter_keys
FROM warehouse.fact_observation;
