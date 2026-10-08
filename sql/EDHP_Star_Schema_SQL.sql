-- ============================================================
-- UC18 - ENTERPRISE HEALTHCARE DATA PLATFORM
-- SPRINT 2 - STAR SCHEMA
-- PostgreSQL DATA WAREHOUSE
-- ============================================================


-- ============================================================
-- 1. CREATE WAREHOUSE SCHEMA
-- ============================================================

CREATE SCHEMA IF NOT EXISTS healthcare;


-- ============================================================
-- 2. DROP EXISTING STAR SCHEMA TABLES
-- ============================================================

DROP TABLE IF EXISTS warehouse.fact_warehouse CASCADE;
DROP TABLE IF EXISTS warehouse.fact_shipment CASCADE;
DROP TABLE IF EXISTS warehouse.fact_procurement CASCADE;
DROP TABLE IF EXISTS warehouse.fact_order CASCADE;

DROP TABLE IF EXISTS healthcare.patients CASCADE;
DROP TABLE IF EXISTS healthcare.encounters CASCADE;
DROP TABLE IF EXISTS healthcare.organizations CASCADE;
DROP TABLE IF EXISTS healthcare.providers CASCADE;
DROP TABLE IF EXISTS healthcare.payers CASCADE;
DROP TABLE IF EXISTS healthcare.payer_transitions CASCADE;
DROP TABLE IF EXISTS healthcare.medications CASCADE;
DROP TABLE IF EXISTS healthcare.immunizations CASCADE;
DROP TABLE IF EXISTS healthcare.observations CASCADE;
DROP TABLE IF EXISTS healthcare.allergies CASCADE;
DROP TABLE IF EXISTS healthcare.conditions CASCADE;
DROP TABLE IF EXISTS healthcare.procedures CASCADE;
DROP TABLE IF EXISTS healthcare.devices CASCADE;



-- ============================================================
-- 3. PATIENT DIMENSION
-- ============================================================

CREATE TABLE healthcare.patients (

    id                      VARCHAR(50) PRIMARY KEY,

    birthdate               DATE,

    deathdate               DATE,

    ssn                     VARCHAR(11),

    drivers                 VARCHAR(9),

    prefix                  VARCHAR(5),

    first_                  VARCHAR(20),

    last_                   VARCHAR(20),

    suffix                  VARCHAR(5),

    maiden                  VARCHAR(20),

    marital                 VARCHAR(1),

    race                    VARCHAR(20),

    ethnicity               VARCHAR(20),

    gender                  VARCHAR(1),

    address_                VARCHAR(100),

    city                    VARCHAR(20),

    state_                  VARCHAR(2),

    county                  VARCHAR(20),

    zip                     INTEGER(5),

    lat                     NUMERIC(9,9),

    lon                     NUMERIC(9,9),

    healthcare_expenses     NUMERIC(9,9),

    healthcare_coverage     NUMERIC(9,9)

);


-- ============================================================
-- 4. ORGANIZATION DIMENSION
-- ============================================================

CREATE TABLE healthcare.organizations (

    id                      VARCHAR(50) PRIMARY KEY,

    name_                   VARCHAR(100),

    address_                VARCHAR(100),

    city                    VARCHAR(20),

    state_                  VARCHAR(2),

    zip                     INTEGER(5),

    lat                     NUMERIC(9,9),

    lon                     NUMERIC(9,9),

    phone                   INTEGER(10),

    revenue                 NUMERIC(9,9),

    utilization             INTEGER(8)

);


-- ============================================================
-- 5. PROVIDERS DIMENSION
-- ============================================================

CREATE TABLE healthcare.providers (

    id                      VARCHAR(50) PRIMARY KEY,

    organization_id         VARCHAR(50),

    name_                   VARCHAR(100),

    gender                  VARCHAR(1),

    speciality              VARCHAR(30),

    address_                VARCHAR(100),

    city                    VARCHAR(20),

    state_                  VARCHAR(2),

    zip                     INTEGER(5),

    lat                     VARCHAR(50),

    lon                     VARCHAR(100),

    utilization             VARCHAR(255),

    FOREIGN KEY (organization_id) REFERENCES healthcare.organizations(id);

);


-- ============================================================
-- 6. PAYERS DIMENSION
-- ============================================================

CREATE TABLE healthcare.payers (

    id                      VARCHAR(50) PRIMARY KEY,

    name_                   VARCHAR(20),

    address_                VARCHAR(100),

    city                    VARCHAR(20),

    state_headquartered     VARCHAR(2),

    zip                     INTEGER(5),

    phone                   VARCHAR(14),

    amount_covered          NUMERIC(8,3),

    amount_uncovered        NUMERIC(8,3),

    revenue                 INTEGER(9),

    covered_encounters      INTEGER(6),

    uncovered_encounters    INTEGER(6),

    covered_medications     INTEGER(6),

    uncovered_medications   INTEGER(6),

    covered_procedures      INTEGER(6),

    uncovered_procedures    INTEGER(6),

    covered_immunizations   INTEGER(6),

    uncovered_immunizations INTEGER(6),

    unique_customers        INTEGER(5),

    qols_average            NUMERIC(2,9),

    member_months           INTEGER(6)

);


-- ============================================================
-- 7. PAYER TRANSITIONS DIMENSION
-- ============================================================

CREATE TABLE healthcare.payer_transitions (

    patient_id              VARCHAR,

    start_year              YEAR(4),

    end_year                YEAR(4),

    payer_id                VARCHAR,

    ownership_              VARCHAR(15),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (payer_id) REFERENCES healthcare.payers(id),
);


-- ============================================================
-- 8. ENCOUNTERS DIMENSION
-- ============================================================

CREATE TABLE healthcare.encounters (

    id                      VARCHAR(50) PRIMARY KEY,

    start_                  DATE,

    end_                    DATE,

    patient_id              VARCHAR,

    organization_id         VARCHAR,

    provider_id             VARCHAR,

    payer_id                VARCHAR,

    encounterclass          VARCHAR(20),

    code                    INTEGER(9) NOT NULL,

    description_            VARCHAR(50),

    base_encounter_cost     NUMERIC(8,3),

    total_claim_cost        NUMERIC(8,3),

    payer_coverage          NUMERIC(8,3),

    reasoncode              INTEGER(9),

    reasondescription       VARCHAR(50),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (organization_id) REFERENCES healthcare.organizations(id),
    FOREIGN KEY (provider_id) REFERENCES healthcare.providers(id),
    FOREIGN KEY (payer_id) REFERENCES healthcare.payers(id)

);


-- ============================================================
-- 9. MEDICATIONS DIMENSION
-- ============================================================

CREATE TABLE healthcare.medications (

    start_                     DATE,

    stop_                      DATE,

    patient_id                 VARCHAR,

    payer_id                   VARCHAR,

    encounter_id               VARCHAR,

    code                       INTEGER(9) NOT NULL,

    description_               VARCHAR(50),

    base_cost                  NUMERIC(8,3),

    payer_coverage             NUMERIC(8,3),

    dispenses                  INTEGER(3),

    totalcost                  NUMERIC(8,3),

    reasoncode                 INTEGER(9),

    reasondescription          VARCHAR(50)

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (payer_id) REFERENCES healthcare.payers(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id)

);


-- ============================================================
-- 10. CONDITIONS DIMENSION
-- ============================================================

CREATE TABLE healthcare.conditions (

    start_                  DATE NOT NULL,

    stop_                   DATE,

    patient_id              VARCHAR,

    encounter_id            VARCHAR,

    code                    INTEGER(9) NOT NULL,

    description_            VARCHAR(50),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id)

);


-- ============================================================
-- 11. ALLERGIES DIMENSION
-- ============================================================

CREATE TABLE healthcare.allergies (

    start_                      DATE NOT NULL,

    stop_                       DATE,

    patient_id                  VARCHAR,

    encounter_id                VARCHAR,

    code                        INTEGER(9) NOT NULL,

    description_                VARCHAR(50),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id)

);


-- ============================================================
-- 12. OBSERVATIONS DIMENSION
-- ============================================================

CREATE TABLE healthcare.observations (

    date_                   DATE NOT NULL,

    patient_id              VARCHAR,

    encounter_id            VARCHAR,

    code                    VARCHAR(9) NOT NULL,

    description_            VARCHAR(50),

    value_                  NUMERIC(5,4),

    units                   VARCHAR(10),

    type_                   VARCHAR(12),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id)

);


-- ============================================================
-- 13. PROCEDURES DIMENSION
-- ============================================================

CREATE TABLE healthcare.procedures (

    date_                       DATE NOT NULL,

    patient_id                  VARCHAR,

    encounter_id                VARCHAR,

    code                        INTEGER(9) NOT NULL,

    description_                VARCHAR(50),

    base_cost                   NUMERIC(8,3),

    reasoncode                  INTEGER(9),

    reasondescription           VARCHAR(50),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id),

);


-- ============================================================
-- 14. IMAGING_STUDIES DIMENSIONS
-- ============================================================

CREATE TABLE healthcare.imaging_studies (

    id                            VARCHAR(50) PRIMARY KEY,

    date_                         DATE,

    patient_id                    VARCHAR,

    encounter_id                  VARCHAR,

    bodysite_code                 INTEGER(9),

    bodysite_description          VARCHAR(20),

    modality_code                 VARCHAR(2),

    modality_description          VARCHAR(20),

    sop_code                      VARCHAR(50),

    sop_description               VARCHAR(50),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id)

);

-- ============================================================
-- 15. DEVICES DIMENSIONS
-- ============================================================

CREATE TABLE healthcare.devices (

    start_                        DATE,

    stop_                         DATE,

    patient_id                    VARCHAR,

    encounter_id                  VARCHAR,

    code                          INTEGER(9) NOT NULL,

    description_                  VARCHAR(50),

    udi                           VARCHAR(100),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id)

)

-- ============================================================
-- 16. IMMUNIZATIONS DIMENSIONS
-- ============================================================

CREATE TABLE healthcare.immunizations (

    date_                         DATE,

    patient_id                    VARCHAR,

    encounter_id                  VARCHAR,

    code                          INTEGER(5) NOT NULL,

    description_                  VARCHAR(50),

    base_cost                     NUMERIC(8,3),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id)

)

-- ============================================================
-- 17. CAREPLANS DIMENSIONS
-- ============================================================

CREATE TABLE healthcare.careplans (

    id                            VARCHAR(50) PRIMARY KEY,

    start_                        DATE NOT NULL,

    stop_                         DATE,

    patient_id                    VARCHAR,

    encounter_id                  VARCHAR,

    code                          INTEGER(20),

    description_                  VARCHAR(50),

    reasoncode                    INTEGER(9),

    reasondescription             VARCHAR(50),

    FOREIGN KEY (patient_id) REFERENCES healthcare.patients(id),
    FOREIGN KEY (encounter_id) REFERENCES healthcare.encounters(id)

)