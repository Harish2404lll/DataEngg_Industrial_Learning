-- =====================================================
-- ENTERPRISE HEALTHCARE DATA PLATFORM (UC2)
-- PostgreSQL Source / Raw Dataset Schemas
-- Schema: public
-- =====================================================

-- 1. PATIENTS
CREATE TABLE uc2_patients (
    patient_id VARCHAR(100),
    birthdate DATE,
    deathdate DATE,
    ssn VARCHAR(20),
    drivers VARCHAR(50),
    passport VARCHAR(50),
    prefix VARCHAR(30),
    first VARCHAR(100),
    last VARCHAR(100),
    suffix VARCHAR(30),
    maiden VARCHAR(100),
    marital VARCHAR(10),
    race VARCHAR(50),
    ethnicity VARCHAR(50),
    gender VARCHAR(20),
    birthplace TEXT,
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(100),
    county VARCHAR(100),
    zip VARCHAR(20),
    latitude NUMERIC(10,6),
    longitude NUMERIC(10,6),
    healthcare_expenses NUMERIC(15,2),
    healthcare_coverage NUMERIC(15,2)
);

-- 2. ENCOUNTERS
CREATE TABLE uc2_encounters (
    encounter_id VARCHAR(100),
    start_date TIMESTAMP,
    stop_date TIMESTAMP,
    patient_id VARCHAR(100),
    organization_id VARCHAR(100),
    provider_id VARCHAR(100),
    payer_id VARCHAR(100),
    encounter_class VARCHAR(50),
    code VARCHAR(50),
    description TEXT,
    base_encounter_cost NUMERIC(15,2),
    total_claim_cost NUMERIC(15,2),
    payer_coverage NUMERIC(15,2),
    reason_code VARCHAR(50),
    reason_description TEXT
);

-- 3. CONDITIONS
CREATE TABLE uc2_conditions (
    start_date DATE,
    stop_date DATE,
    patient_id VARCHAR(100),
    encounter_id VARCHAR(100),
    code VARCHAR(50),
    description TEXT
);

-- 4. OBSERVATIONS
CREATE TABLE uc2_observations (
    date TIMESTAMP,
    patient_id VARCHAR(100),
    encounter_id VARCHAR(100),
    category VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    value TEXT,
    units VARCHAR(50),
    type VARCHAR(30)
);

-- 5. MEDICATIONS
CREATE TABLE uc2_medications (
    start_date TIMESTAMP,
    stop_date TIMESTAMP,
    patient_id VARCHAR(100),
    payer_id VARCHAR(100),
    encounter_id VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    base_cost NUMERIC(15,2),
    payer_coverage NUMERIC(15,2),
    dispenses INTEGER,
    total_cost NUMERIC(15,2),
    reason_code VARCHAR(50),
    reason_description TEXT
);

-- 6. PROCEDURES
CREATE TABLE uc2_procedures (
    date TIMESTAMP,
    patient_id VARCHAR(100),
    encounter_id VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    base_cost NUMERIC(15,2),
    reason_code VARCHAR(50),
    reason_description TEXT
);

-- 7. ALLERGIES
CREATE TABLE uc2_allergies (
    start_date DATE,
    stop_date DATE,
    patient_id VARCHAR(100),
    encounter_id VARCHAR(100),
    code VARCHAR(50),
    description TEXT
);

-- 8. IMMUNIZATIONS
CREATE TABLE uc2_immunizations (
    date TIMESTAMP,
    patient_id VARCHAR(100),
    encounter_id VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    base_cost NUMERIC(15,2)
);

-- 9. CAREPLANS
CREATE TABLE uc2_careplans (
    careplan_id VARCHAR(100),
    start_date DATE,
    stop_date DATE,
    patient_id VARCHAR(100),
    encounter_id VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    reason_code VARCHAR(50),
    reason_description TEXT
);

-- 10. DEVICES
CREATE TABLE uc2_devices (
    start_date TIMESTAMP,
    stop_date TIMESTAMP,
    patient_id VARCHAR(100),
    encounter_id VARCHAR(100),
    code VARCHAR(50),
    description TEXT,
    udi TEXT
);

-- 11. IMAGING STUDIES
CREATE TABLE uc2_imaging_studies (
    imaging_study_id VARCHAR(100),
    study_date TIMESTAMP,
    patient_id VARCHAR(100),
    encounter_id VARCHAR(100),
    bodysite_code VARCHAR(50),
    bodysite_description TEXT,
    modality_code VARCHAR(20),
    modality_description TEXT,
    sop_code VARCHAR(100),
    sop_description TEXT
);

-- 12. ORGANIZATIONS
CREATE TABLE uc2_organizations (
    organization_id VARCHAR(100),
    name VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    latitude NUMERIC(10,6),
    longitude NUMERIC(10,6),
    phone VARCHAR(30),
    revenue NUMERIC(15,2),
    utilization INT
);

-- 13. PAYER TRANSITIONS
CREATE TABLE uc2_payer_transitions (
    patient_id VARCHAR(100),
    start_year INT,
    end_year INT,
    payer_id VARCHAR(100),
    ownership VARCHAR(100)
);

-- 14. PAYERS
CREATE TABLE uc2_payers (
    payer_id VARCHAR(100),
    name VARCHAR(255),
    address TEXT,
    city VARCHAR(100),
    state_headquartered VARCHAR(50),
    zip VARCHAR(20),
    phone VARCHAR(30),
    amount_covered DECIMAL(15,2),
    amount_uncovered DECIMAL(15,2),
    revenue DECIMAL(15,2),
    covered_encounters INTEGER,
    uncovered_encounters INTEGER,
    covered_medications INTEGER,
    uncovered_medications INTEGER,
    covered_procedures INTEGER,
    uncovered_procedures INTEGER,
    covered_immunizations INTEGER,
    uncovered_immunizations INTEGER,
    unique_customers INTEGER,
    qols_avg DECIMAL(15,10),
    member_months INTEGER
);

-- 15. PROVIDERS
CREATE TABLE uc2_providers (
    provider_id VARCHAR(100),
    organization_id VARCHAR(100),
    name VARCHAR(255),
    gender VARCHAR(20),
    speciality VARCHAR(150),
    address TEXT,
    city VARCHAR(100),
    state VARCHAR(50),
    zip VARCHAR(20),
    latitude DECIMAL(10,6),
    longitude DECIMAL(10,6),
    utilization INTEGER
);