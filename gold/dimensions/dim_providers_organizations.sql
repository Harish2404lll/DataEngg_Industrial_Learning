-- UC2 Sprint 2 | Provider and organization reporting view
-- Assumes warehouse.dim_provider and warehouse.dim_organization share organization_id.
CREATE SCHEMA IF NOT EXISTS gold;
CREATE OR REPLACE VIEW gold.dim_providers_organizations AS
SELECT p.*, o.name AS organization_name
FROM warehouse.dim_provider AS p
LEFT JOIN warehouse.dim_organization AS o
  ON p.organization_id = o.organization_id;
