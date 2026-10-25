-- UC2 Sprint 2 | Careplan status mart
-- A stop date indicates an ended careplan, not proof of clinical success.
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.mrt_careplan_outcomes AS
SELECT careplan_id, patient_id, encounter_id, code, description,
       start_date, stop_date,
       CASE WHEN stop_date IS NOT NULL THEN 'ended'
            ELSE 'ongoing_or_missing_stop_date'
       END AS careplan_status,
       reason_code, reason_description
FROM public.uc2_careplans;
