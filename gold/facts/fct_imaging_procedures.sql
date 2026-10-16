-- UC2 Sprint 2 | Imaging and procedure events
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.fct_imaging_procedures AS
SELECT 'imaging'::text AS event_type, patient_id, encounter_id, study_date AS event_timestamp,
       bodysite_code AS code, bodysite_description AS description,
       modality_code AS category_code, modality_description AS category_description
FROM public.uc2_imaging_studies
UNION ALL
SELECT 'procedure'::text, patient_id, encounter_id, date AS event_timestamp,
       code, description, NULL::varchar(50), NULL::text
FROM public.uc2_procedures;
