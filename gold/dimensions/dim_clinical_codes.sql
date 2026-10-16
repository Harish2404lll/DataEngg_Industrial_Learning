-- UC2 Sprint 2 | Distinct clinical codes from Synthea source tables
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.dim_clinical_codes AS
SELECT DISTINCT code, description, 'condition'::text AS source_type
FROM public.uc2_conditions WHERE code IS NOT NULL
UNION
SELECT DISTINCT code, description, 'observation'::text
FROM public.uc2_observations WHERE code IS NOT NULL
UNION
SELECT DISTINCT code, description, 'medication'::text
FROM public.uc2_medications WHERE code IS NOT NULL
UNION
SELECT DISTINCT code, description, 'procedure'::text
FROM public.uc2_procedures WHERE code IS NOT NULL
UNION
SELECT DISTINCT code, description, 'allergy'::text
FROM public.uc2_allergies WHERE code IS NOT NULL
UNION
SELECT DISTINCT code, description, 'immunization'::text
FROM public.uc2_immunizations WHERE code IS NOT NULL
UNION
SELECT DISTINCT code, description, 'careplan'::text
FROM public.uc2_careplans WHERE code IS NOT NULL
UNION
SELECT DISTINCT code, description, 'device'::text
FROM public.uc2_devices WHERE code IS NOT NULL;
