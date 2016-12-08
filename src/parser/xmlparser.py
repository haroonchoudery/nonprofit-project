"""
This module provides the functionalities to process an electronic filing in xml
format. This module will extract and return the interested element values based
on the form type. It is worth noticing that the element naming may be inconsistent
across different form type.
"""

import urllib2
from lxml import etree
from collections import defaultdict

# Predefined xml paths common to Form 990 and Form 990EZ
TAX_YEAR = './/{http://www.irs.gov/efile}TaxYr'

# Predefined xml paths for interested elements for 990 form
CY_TOTAL_REVENUE = './/{http://www.irs.gov/efile}CYTotalRevenueAmt'
PY_TOTAL_REVENUE = './/{http://www.irs.gov/efile}PYTotalRevenueAmt'
CY_CONTRIBUTIONS = './/{http://www.irs.gov/efile}CYContributionsGrantsAmt'
PY_CONTRIBUTIONS = './/{http://www.irs.gov/efile}PYContributionsGrantsAmt'
CY_SERVICE_REV = './/{http://www.irs.gov/efile}CYProgramServiceRevenueAmt'
PY_SERVICE_REV = './/{http://www.irs.gov/efile}PYProgramServiceRevenueAmt'
CY_INVESTMENT_INCOME = './/{http://www.irs.gov/efile}PYProgramServiceRevenueAmt'
PY_INVESTMENT_INCOME = './/{http://www.irs.gov/efile}PYProgramServiceRevenueAmt'

# Predefined xml paths for interested elements for 990EZ form
CY_TOTAL_REVENUE_EZ = './/{http://www.irs.gov/efile}TotalRevenueAmt'
CY_CONTRIBUTIONS_EZ = './/{http://www.irs.gov/efile}ContributionsGiftsGrantsEtcAmt'
CY_SERVICE_REV_EZ = './/{http://www.irs.gov/efile}ProgramServiceRevenueAmt'
CY_INVESTMENT_INCOME_EZ = './/{http://www.irs.gov/efile}GrossInvestmentIncome509Grp'
CY_GRANTS_PAID = './/{http://www.irs.gov/efile}GrantsAndAllocationsAmt'

def parse_xml_form(url, form_type):
    tree = etree.ElementTree(file=urllib2.urlopen(url))
    root=tree.getroot()

    if form_type == '990':
        fields = get_990_fields(root)
    elif form_type == '990EZ':
        fields = get_990ez_fields(root)

    fields['organization_type'] = get_organization_type(root)
    fields['tax_year'] = get_field_abstract(root, TAX_YEAR)
    return fields

def get_990_fields(root):
    fields = defaultdict(lambda: None)
    fields['cy_total_revenue'] = get_field_abstract(root, CY_TOTAL_REVENUE)
    fields['py_total_revenue'] = get_field_abstract(root, PY_TOTAL_REVENUE)
    fields['cy_contributions'] = get_field_abstract(root, CY_CONTRIBUTIONS)
    fields['py_contributions'] = get_field_abstract(root, PY_CONTRIBUTIONS)
    fields['cy_service_revenue'] = get_field_abstract(root, CY_SERVICE_REV)
    fields['py_service_revenue'] = get_field_abstract(root, PY_SERVICE_REV)
    return fields

def get_990ez_fields(root):
    fields = defaultdict(lambda: None)
    fields['cy_total_revenue'] = get_field_abstract(root, CY_TOTAL_REVENUE_EZ)
    fields['cy_contributions'] = get_field_abstract(root, CY_CONTRIBUTIONS_EZ)
    fields['cy_service_revenue'] = get_field_abstract(root, CY_SERVICE_REV_EZ)
    return fields

def get_field_abstract(root, field):
    value = root.find(field)
    return value.text if value is not None else None

def get_organization_type(root):
    """This function will return the organization type.

    Unlike other fields, the organization type is represneted as a xml element
    name instead of an element value. We will use the below regex to extract it.
    """
    type_regex = "//*[re:test(local-name(), '^Organization.*')]"
    organization_tag = root.xpath(type_regex, namespaces={'re': "http://exslt.org/regular-expressions"})[0].tag
    if organization_tag is None:
        return None
    else:
        organization_type = organization_tag.split('Organization')[1]
        return organization_type
