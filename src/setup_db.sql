# Create the database
CREATE DATABASE IF NOT EXISTS organizations;
USE organizations;

# Create the primary table to store the data of tax-exempt organizations.
# IF it alreay exists in the database, remove it and recreate it.
DROP TABLE IF EXISTS tax_exempt_organizations;
CREATE TABLE tax_exempt_organizations (
  electronic_id INT NOT NULL,
  organization_name TEXT,
  organization_type TEXT,
  current_year_revenue INT,
  prior_year_revenue INT,
  annual_revenue_growth FLOAT(4,2),
  PRIMARY KEY (electronic_id)
);
