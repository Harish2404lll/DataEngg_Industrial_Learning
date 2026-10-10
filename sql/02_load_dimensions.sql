-- EHDP Sprint 2: load dimensions.
-- Run after 01_create_warehouse_tables.sql.
-- DISTINCT ON removes repeated IDs from dimension loads; ON CONFLICT allows safe reruns.

INSERT INTO warehouse.dim_patient
(patient_id,birth_date,death_date,gender,race,ethnicity,marital_status,city,state,zip)
SELECT DISTINCT ON (patient_id)
 patient_id,birth_date,death_date,gender,race,ethnicity,marital_status,city,state,zip
FROM public.uc2_patients WHERE patient_id IS NOT NULL
ORDER BY patient_id ON CONFLICT (patient_id) DO NOTHING;

INSERT INTO warehouse.dim_organization
(organization_id,organization_name,city,state,zip,revenue,utilization)
SELECT DISTINCT ON (organization_id)
 organization_id,name,city,state,zip,revenue,utilization
FROM public.uc2_organizations WHERE organization_id IS NOT NULL
ORDER BY organization_id ON CONFLICT (organization_id) DO NOTHING;

INSERT INTO warehouse.dim_payer
(payer_id,payer_name,city,state_headquartered,zip,amount_covered,amount_uncovered,revenue)
SELECT DISTINCT ON (payer_id)
 payer_id,name,city,state_headquartered,zip,amount_covered,amount_uncovered,revenue
FROM public.uc2_payers WHERE payer_id IS NOT NULL
ORDER BY payer_id ON CONFLICT (payer_id) DO NOTHING;

-- Organizations must exist before provider rows are loaded.
INSERT INTO warehouse.dim_provider
(provider_id,organization_id,provider_name,gender,speciality,city,state,zip)
SELECT DISTINCT ON (provider_id)
 provider_id,organization_id,name,gender,speciality,city,state,zip
FROM public.uc2_providers WHERE provider_id IS NOT NULL
ORDER BY provider_id ON CONFLICT (provider_id) DO NOTHING;

INSERT INTO warehouse.dim_date
(date_key,full_date,year_number,quarter_number,month_number,month_name,day_number)
SELECT DISTINCT TO_CHAR(d,'YYYYMMDD')::INTEGER,d,
 EXTRACT(YEAR FROM d)::INTEGER,EXTRACT(QUARTER FROM d)::INTEGER,
 EXTRACT(MONTH FROM d)::INTEGER,TRIM(TO_CHAR(d,'Month')),EXTRACT(DAY FROM d)::INTEGER
FROM (
 SELECT start_time::date AS d FROM public.uc2_encounters WHERE start_time IS NOT NULL
 UNION
 SELECT stop_time::date FROM public.uc2_encounters WHERE stop_time IS NOT NULL
 UNION
 SELECT observation_date::date FROM public.uc2_observations WHERE observation_date IS NOT NULL
) dates
WHERE d IS NOT NULL
ON CONFLICT (date_key) DO NOTHING;

SELECT 'dim_patient' AS table_name,COUNT(*) AS row_count FROM warehouse.dim_patient
UNION ALL SELECT 'dim_organization',COUNT(*) FROM warehouse.dim_organization
UNION ALL SELECT 'dim_provider',COUNT(*) FROM warehouse.dim_provider
UNION ALL SELECT 'dim_payer',COUNT(*) FROM warehouse.dim_payer
UNION ALL SELECT 'dim_date',COUNT(*) FROM warehouse.dim_date
ORDER BY table_name;
