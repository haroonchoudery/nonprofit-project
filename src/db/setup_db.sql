# Create the database
CREATE DATABASE IF NOT EXISTS organizations;
USE organizations;

# Create the primary table to store the data of tax-exempt organizations
CREATE TABLE IF NOT EXISTS tax_exempt_organizations (
  electronic_id INT NOT NULL,
  organization_name TEXT,
  organization_type TEXT,
  cy_total_revenue INT,
  py_total_revenue INT,
  cy_contribution INT,
  py_contribution INT,
  cy_service_revenue INT,
  py_service_revenue INT,
  annual_totoal_revenue_growth FLOAT(4,2),
  PRIMARY KEY (electronic_id)
);
