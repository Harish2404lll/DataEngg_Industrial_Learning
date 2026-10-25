-- UC2 Sprint 2 | Medication and immunization events
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.fct_medications_immunizations AS
SELECT 'medication'::text AS event_type, patient_id, encounter_id,
       start_date AS event_timestamp, stop_date, code, description,
       total_cost::numeric AS cost
FROM public.uc2_medications
UNION ALL
SELECT 'immunization'::text, patient_id, encounter_id, date AS event_timestamp,
       NULL::timestamp, code, description, base_cost::numeric
FROM public.uc2_immunizations;
