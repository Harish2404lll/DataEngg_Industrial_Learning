-- EHDP Sprint 2: create warehouse star schema.
-- Source tables public.uc2_* are not modified.
CREATE SCHEMA IF NOT EXISTS warehouse;

CREATE TABLE IF NOT EXISTS warehouse.dim_patient (
 patient_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 patient_id VARCHAR(50) NOT NULL UNIQUE, birth_date DATE, death_date DATE,
 gender VARCHAR(10), race VARCHAR(50), ethnicity VARCHAR(50),
 marital_status VARCHAR(10), city VARCHAR(100), state VARCHAR(100), zip VARCHAR(20)
);
CREATE TABLE IF NOT EXISTS warehouse.dim_organization (
 organization_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 organization_id VARCHAR(100) NOT NULL UNIQUE, organization_name VARCHAR(255),
 city VARCHAR(100), state VARCHAR(50), zip VARCHAR(20), revenue NUMERIC, utilization INTEGER
);
CREATE TABLE IF NOT EXISTS warehouse.dim_provider (
 provider_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 provider_id VARCHAR(100) NOT NULL UNIQUE, organization_id VARCHAR(100),
 provider_name VARCHAR(255), gender VARCHAR(20), speciality VARCHAR(150),
 city VARCHAR(100), state VARCHAR(50), zip VARCHAR(20),
 CONSTRAINT fk_provider_organization FOREIGN KEY (organization_id)
 REFERENCES warehouse.dim_organization(organization_id)
);
CREATE TABLE IF NOT EXISTS warehouse.dim_payer (
 payer_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 payer_id VARCHAR(100) NOT NULL UNIQUE, payer_name VARCHAR(255),
 city VARCHAR(100), state_headquartered VARCHAR(50), zip VARCHAR(20),
 amount_covered NUMERIC, amount_uncovered NUMERIC, revenue NUMERIC
);
CREATE TABLE IF NOT EXISTS warehouse.dim_date (
 date_key INTEGER PRIMARY KEY, full_date DATE NOT NULL UNIQUE,
 year_number INTEGER NOT NULL, quarter_number INTEGER NOT NULL,
 month_number INTEGER NOT NULL, month_name VARCHAR(20) NOT NULL,
 day_number INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS warehouse.fact_encounter (
 encounter_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 encounter_id VARCHAR(50) NOT NULL UNIQUE,
 patient_key BIGINT NOT NULL REFERENCES warehouse.dim_patient(patient_key),
 organization_key BIGINT REFERENCES warehouse.dim_organization(organization_key),
 provider_key BIGINT REFERENCES warehouse.dim_provider(provider_key),
 payer_key BIGINT REFERENCES warehouse.dim_payer(payer_key),
 start_date_key INTEGER REFERENCES warehouse.dim_date(date_key),
 stop_date_key INTEGER REFERENCES warehouse.dim_date(date_key),
 encounter_class VARCHAR(30), code VARCHAR(30), description VARCHAR(255),
 base_encounter_cost NUMERIC, total_claim_cost NUMERIC, payer_coverage NUMERIC,
 reason_code VARCHAR(30), reason_description VARCHAR(255)
);
CREATE TABLE IF NOT EXISTS warehouse.fact_observation (
 observation_key BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
 observation_date_key INTEGER REFERENCES warehouse.dim_date(date_key),
 patient_key BIGINT NOT NULL REFERENCES warehouse.dim_patient(patient_key),
 encounter_key BIGINT REFERENCES warehouse.fact_encounter(encounter_key),
 observation_code VARCHAR(50), description VARCHAR(255), observation_value TEXT,
 units VARCHAR(50), observation_type VARCHAR(50)
);

-- Confirm the seven warehouse tables.
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'warehouse' AND table_type = 'BASE TABLE'
ORDER BY table_name;
