-- UC2 Sprint 2 | Patient summary mart
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.mrt_patient_health_summary AS
WITH encounter_summary AS (
    SELECT patient_id, COUNT(*) AS encounter_count
    FROM public.uc2_encounters GROUP BY patient_id
),
observation_summary AS (
    SELECT patient_id, COUNT(*) AS observation_count
    FROM public.uc2_observations GROUP BY patient_id
),
condition_summary AS (
    SELECT patient_id, COUNT(*) AS condition_count
    FROM public.uc2_conditions GROUP BY patient_id
)
SELECT p.patient_id, p.birthdate, p.gender, p.city, p.state,
       COALESCE(e.encounter_count, 0) AS encounter_count,
       COALESCE(o.observation_count, 0) AS observation_count,
       COALESCE(c.condition_count, 0) AS condition_count
FROM public.uc2_patients p
LEFT JOIN encounter_summary e USING (patient_id)
LEFT JOIN observation_summary o USING (patient_id)
LEFT JOIN condition_summary c USING (patient_id);
