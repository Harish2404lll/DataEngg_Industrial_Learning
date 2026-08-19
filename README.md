# Enterprise Healthcare Data Platform (EHDP): Building a Unified Clinical & Hospital Analytics Platform 
This repository is dedicated to organizing and maintaining our project work, code, datasets, and documentation.

## 📊 Dataset Information

The datasets used in this project are sourced entirely from **Synthea**, an open-source synthetic healthcare data generator.

### Dataset Source

* **Source:** Synthea
* **Data Type:** Synthetic Healthcare Data
* **Format:** CSV
* **Purpose:** Simulates realistic hospital and patient healthcare records without using real patient information.

### Healthcare Data Covered

The Synthea datasets provide information related to:

* Patient demographics and registration
* Clinical encounters and EHR records
* Medical conditions and allergies
* Laboratory and clinical observations
* Medications and pharmacy-related data
* Procedures and care plans
* Insurance and payer information
* Healthcare costs and billing-related information
* Medical devices
* Imaging studies
* Providers and healthcare organizations

### Data Integration

The datasets are related using common identifiers such as:

`Patient ID → Encounter ID → Clinical / Operational Records`

Additional identifiers such as **Provider ID, Organization ID, Payer ID, and Imaging Study ID** help establish relationships across the healthcare data.

This connected structure allows the project to simulate data from multiple hospital systems and build a unified **Enterprise Healthcare Data Platform (EHDP)** for data engineering and analytics.
