/*
I remove the tax_year because we agree that we are only going to look at
the most recent tax form, so we do not need the tax year to query a
organization. I also extend the schema to include the new added items.
*/

# Create the database
CREATE DATABASE IF NOT EXISTS organizations;
USE organizations;

# Create the primary table to store the data of tax-exempt organizations
CREATE TABLE IF NOT EXISTS tax_exempt_organizations (
  electronic_id INT NOT NULL,
  form_type VARCHAR(10) NOT NULL,
  organization_name TEXT,
  organization_type TEXT,
  cy_total_revenue INT,
  py_total_revenue INT,
  cy_service_revenue INT,
  py_service_revenue INT,
  cy_contributions INT,
  py_contributions INT,
  annual_totoal_revenue_growth FLOAT(4,2),
  annual_service_revenue_growth FLOAT(4,2),
  annual_contributions_growth FLOAT(4,2),
  PRIMARY KEY (electronic_id)
);
