/*
I remove the tax_year because we agree that we are only going to look at
the most recent tax form, so we do not need the tax year to query a
organization. I also extend the schema to include the new added items.

Alex: I am adding back the tax year even though it might not be important to the scope of this particular application. The table should be robust for the business use and we should be able to handle multiple tax years for a single organization. I am creating views to handle the front end queries so this should be transparent (the view will only contain the most recent data).

*/

# Create the database
CREATE DATABASE IF NOT EXISTS organizations;
USE organizations;

# Create the primary table to store the data of tax-exempt organizations
CREATE TABLE IF NOT EXISTS tax_exempt_organizations (
  electronic_id INT NOT NULL,
  tax_year INT NOT NULL,
  form_type VARCHAR(10) NOT NULL,
  organization_name TEXT,
  organization_type TEXT,
  cy_total_revenue INT,
  py_total_revenue INT,
  cy_service_revenue INT,
  py_service_revenue INT,
  cy_contributions INT,
  py_contributions INT,
  annual_total_revenue_growth FLOAT(4,2),
  annual_service_revenue_growth FLOAT(4,2),
  annual_contributions_growth FLOAT(4,2),
  PRIMARY KEY (electronic_id, tax_year)
);

CREATE OR REPLACE VIEW max_years as (
  SELECT electronic_id, max(tax_year) tax_year
  FROM tax_exempt_organizations
  GROUP BY electronic_id
);


CREATE OR REPLACE VIEW tax_exempt_organizations_current AS (
  select teo.*
  FROM tax_exempt_organizations teo
  INNER JOIN max_years my
    ON teo.electronic_id = my.electronic_id
    AND teo.tax_year = my.tax_year
);
