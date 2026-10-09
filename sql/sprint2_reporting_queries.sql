-- EHDP Sprint 2 analytical SQL queries. Run after warehouse loads.

-- 1. Encounter count and claim cost by year/month.
SELECT EXTRACT(YEAR FROM encounter_date)::int AS year,
 EXTRACT(MONTH FROM encounter_date)::int AS month, COUNT(*) AS encounter_count,
 SUM(total_claim_cost) AS total_claim_cost, AVG(total_claim_cost) AS average_claim_cost
FROM warehouse.fact_encounter GROUP BY 1,2 ORDER BY 1,2;

-- 2. Encounter volume and cost by organization.
SELECT o.organization_name, COUNT(*) AS encounter_count,
 SUM(f.total_claim_cost) AS total_claim_cost, AVG(f.total_claim_cost) AS average_claim_cost
FROM warehouse.fact_encounter f
LEFT JOIN warehouse.dim_organization o ON o.organization_id=f.organization_id
GROUP BY o.organization_name ORDER BY encounter_count DESC;

-- 3. Encounter volume by payer.
SELECT p.payer_name, COUNT(*) AS encounter_count,
 SUM(f.payer_coverage) AS total_payer_coverage, SUM(f.total_claim_cost) AS total_claim_cost
FROM warehouse.fact_encounter f LEFT JOIN warehouse.dim_payer p ON p.payer_id=f.payer_id
GROUP BY p.payer_name ORDER BY encounter_count DESC;

-- 4. Top ten patients by encounter count (synthetic IDs only).
SELECT patient_id, COUNT(*) AS encounter_count, SUM(total_claim_cost) AS total_claim_cost
FROM warehouse.fact_encounter GROUP BY patient_id ORDER BY encounter_count DESC LIMIT 10;

-- 5. Most frequent observation codes and numeric averages.
SELECT observation_code, description, units, COUNT(*) AS observation_count,
 AVG(value_numeric) AS average_numeric_value
FROM warehouse.fact_observation GROUP BY observation_code,description,units
ORDER BY observation_count DESC LIMIT 25;

-- 6. Basic fact-table quality checks.
SELECT 'fact_encounter' AS table_name, COUNT(*) AS row_count,
 COUNT(*) FILTER (WHERE patient_id IS NULL) AS missing_patient_id,
 COUNT(*) FILTER (WHERE encounter_date IS NULL) AS missing_fact_date
FROM warehouse.fact_encounter
UNION ALL
SELECT 'fact_observation', COUNT(*),
 COUNT(*) FILTER (WHERE patient_id IS NULL),
 COUNT(*) FILTER (WHERE observation_date IS NULL)
FROM warehouse.fact_observation;
