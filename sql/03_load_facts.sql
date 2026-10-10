-- EHDP Sprint 2: load fact tables.
-- Run after 02_load_dimensions.sql.
-- Encounter insert can be rerun safely due to unique encounter_id + ON CONFLICT.
-- IMPORTANT: observation table has no natural unique constraint. Run the observation
-- INSERT only once for initial load; running it again can duplicate observation rows.

INSERT INTO warehouse.fact_encounter
(encounter_id,patient_key,organization_key,provider_key,payer_key,start_date_key,stop_date_key,
 encounter_class,code,description,base_encounter_cost,total_claim_cost,payer_coverage,
 reason_code,reason_description)
SELECT e.encounter_id,dp.patient_key,dor.organization_key,dpr.provider_key,dpy.payer_key,
 TO_CHAR(e.start_time::date,'YYYYMMDD')::INTEGER,
 TO_CHAR(e.stop_time::date,'YYYYMMDD')::INTEGER,
 e.encounter_class,e.code,e.description,e.base_encounter_cost,e.total_claim_cost,
 e.payer_coverage,e.reason_code,e.reason_description
FROM public.uc2_encounters e
JOIN warehouse.dim_patient dp ON e.patient_id=dp.patient_id
LEFT JOIN warehouse.dim_organization dor ON e.organization_id=dor.organization_id
LEFT JOIN warehouse.dim_provider dpr ON e.provider_id=dpr.provider_id
LEFT JOIN warehouse.dim_payer dpy ON e.payer_id=dpy.payer_id
WHERE e.encounter_id IS NOT NULL
ON CONFLICT (encounter_id) DO NOTHING;

-- Initial observation load only; do not rerun on an already-loaded warehouse.
INSERT INTO warehouse.fact_observation
(observation_date_key,patient_key,encounter_key,observation_code,description,
 observation_value,units,observation_type)
SELECT TO_CHAR(o.observation_date::date,'YYYYMMDD')::INTEGER,
 dp.patient_key,fe.encounter_key,o.code,o.description,o.value,o.units,o.type
FROM public.uc2_observations o
JOIN warehouse.dim_patient dp ON o.patient_id=dp.patient_id
LEFT JOIN warehouse.fact_encounter fe ON o.encounter_id=fe.encounter_id
WHERE o.observation_date IS NOT NULL;

SELECT 'fact_encounter' AS table_name,COUNT(*) AS row_count FROM warehouse.fact_encounter
UNION ALL SELECT 'fact_observation',COUNT(*) FROM warehouse.fact_observation
ORDER BY table_name;
