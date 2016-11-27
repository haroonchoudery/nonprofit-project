# Create the database
CREATE DATABASE IF NOT EXISTS organizations;
USE organizations;

# Create the primary table to store the data of tax-exempt organizations
CREATE TABLE IF NOT EXISTS tax_exempt_organizations (
  electronic_id INT NOT NULL,
  name TEXT,
  tax_form_url TEXT,
  type TEXT,
  current_year_revenue INT,
  prior_year_revenue INT,
  annual_revenue_growth NUMERIC,
  PRIMARY KEY (electronic_id)
);
