-- EHDP Sprint 2: read-only validation queries.

-- 1. List relevant tables.
SELECT table_schema,table_name
FROM information_schema.tables
WHERE table_schema IN ('warehouse','healthcare','public') AND table_type='BASE TABLE'
ORDER BY table_schema,table_name;

-- 2. Source row counts.
SELECT 'uc2_patients' AS table_name,COUNT(*) AS row_count FROM public.uc2_patients
UNION ALL SELECT 'uc2_encounters',COUNT(*) FROM public.uc2_encounters
UNION ALL SELECT 'uc2_observations',COUNT(*) FROM public.uc2_observations
UNION ALL SELECT 'uc2_organizations',COUNT(*) FROM public.uc2_organizations
UNION ALL SELECT 'uc2_providers',COUNT(*) FROM public.uc2_providers
UNION ALL SELECT 'uc2_payers',COUNT(*) FROM public.uc2_payers
ORDER BY table_name;

-- 3. Source rows vs unique IDs.
SELECT 'Patients' AS table_name,COUNT(*) AS source_rows,COUNT(DISTINCT patient_id) AS unique_ids
FROM public.uc2_patients
UNION ALL SELECT 'Encounters',COUNT(*),COUNT(DISTINCT encounter_id) FROM public.uc2_encounters
UNION ALL SELECT 'Organizations',COUNT(*),COUNT(DISTINCT organization_id) FROM public.uc2_organizations
UNION ALL SELECT 'Providers',COUNT(*),COUNT(DISTINCT provider_id) FROM public.uc2_providers
UNION ALL SELECT 'Payers',COUNT(*),COUNT(DISTINCT payer_id) FROM public.uc2_payers
ORDER BY table_name;

-- 4. Repeated source IDs, useful for duplicate investigation.
SELECT patient_id,COUNT(*) AS occurrences FROM public.uc2_patients
GROUP BY patient_id HAVING COUNT(*)>1 ORDER BY occurrences DESC LIMIT 20;
SELECT encounter_id,COUNT(*) AS occurrences FROM public.uc2_encounters
GROUP BY encounter_id HAVING COUNT(*)>1 ORDER BY occurrences DESC LIMIT 10;

-- 5. Warehouse row counts.
SELECT 'dim_patient' AS table_name,COUNT(*) AS total_rows FROM warehouse.dim_patient
UNION ALL SELECT 'dim_organization',COUNT(*) FROM warehouse.dim_organization
UNION ALL SELECT 'dim_provider',COUNT(*) FROM warehouse.dim_provider
UNION ALL SELECT 'dim_payer',COUNT(*) FROM warehouse.dim_payer
UNION ALL SELECT 'dim_date',COUNT(*) FROM warehouse.dim_date
UNION ALL SELECT 'fact_encounter',COUNT(*) FROM warehouse.fact_encounter
UNION ALL SELECT 'fact_observation',COUNT(*) FROM warehouse.fact_observation
ORDER BY table_name;

-- 6. Encounter uniqueness.
SELECT COUNT(*) AS warehouse_rows,COUNT(DISTINCT encounter_id) AS unique_encounters
FROM warehouse.fact_encounter;

-- 7. Encounter patient links.
SELECT COUNT(DISTINCT e.encounter_id) AS unique_source_encounters,
 COUNT(DISTINCT e.encounter_id) FILTER (WHERE dp.patient_id IS NOT NULL) AS matching_patients,
 COUNT(DISTINCT e.encounter_id) FILTER (WHERE dp.patient_id IS NULL) AS missing_patients
FROM public.uc2_encounters e
LEFT JOIN warehouse.dim_patient dp ON e.patient_id=dp.patient_id;

-- 8. Encounter organization/provider/payer links.
SELECT COUNT(DISTINCT e.encounter_id) AS unique_encounters,
 COUNT(DISTINCT e.encounter_id) FILTER (WHERE dor.organization_id IS NULL) AS missing_organizations,
 COUNT(DISTINCT e.encounter_id) FILTER (WHERE dpr.provider_id IS NULL) AS missing_providers,
 COUNT(DISTINCT e.encounter_id) FILTER (WHERE dpy.payer_id IS NULL) AS missing_payers
FROM public.uc2_encounters e
LEFT JOIN warehouse.dim_organization dor ON e.organization_id=dor.organization_id
LEFT JOIN warehouse.dim_provider dpr ON e.provider_id=dpr.provider_id
LEFT JOIN warehouse.dim_payer dpy ON e.payer_id=dpy.payer_id;

-- 9. Observation patient/encounter links.
SELECT COUNT(*) AS source_observation_rows,
 COUNT(*) FILTER (WHERE dp.patient_id IS NULL) AS observations_missing_patients,
 COUNT(*) FILTER (WHERE o.encounter_id IS NOT NULL AND fe.encounter_id IS NULL) AS observations_missing_encounters
FROM public.uc2_observations o
LEFT JOIN warehouse.dim_patient dp ON o.patient_id=dp.patient_id
LEFT JOIN warehouse.fact_encounter fe ON o.encounter_id=fe.encounter_id;

-- 10. Encounter date keys: missing values.
SELECT COUNT(*) AS total_encounters,
 COUNT(*) FILTER (WHERE start_date_key IS NULL) AS missing_start_date_key,
 COUNT(*) FILTER (WHERE stop_date_key IS NULL) AS missing_stop_date_key
FROM warehouse.fact_encounter;

-- 11. Encounter date keys: check they match dim_date.
SELECT COUNT(*) FILTER (WHERE sd.date_key IS NULL) AS invalid_start_date_keys,
 COUNT(*) FILTER (WHERE ed.date_key IS NULL) AS invalid_stop_date_keys
FROM warehouse.fact_encounter fe
LEFT JOIN warehouse.dim_date sd ON fe.start_date_key=sd.date_key
LEFT JOIN warehouse.dim_date ed ON fe.stop_date_key=ed.date_key;

-- 12. Observation date keys: check they match dim_date.
SELECT COUNT(*) AS total_observations,
 COUNT(*) FILTER (WHERE dd.date_key IS NULL) AS invalid_observation_date_keys
FROM warehouse.fact_observation fo
LEFT JOIN warehouse.dim_date dd ON fo.observation_date_key=dd.date_key;
