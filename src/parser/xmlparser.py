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
CY_TOTAL_EXPENSES = './/{http://www.irs.gov/efile}CYTotalExpensesAmt'
PY_TOTAL_EXPENSES = './/{http://www.irs.gov/efile}PYTotalExpensesAmt'
CY_GRANTS_PAID = './/{http://www.irs.gov/efile}CYGrantsAndSimilarPaidAmt'
PY_GRANTS_PAID = './/{http://www.irs.gov/efile}PYGrantsAndSimilarPaidAmt'
CY_SALARIES = './/{http://www.irs.gov/efile}CYSalariesCompEmpBnftPaidAmt'
PY_SALARIES = './/{http://www.irs.gov/efile}PYSalariesCompEmpBnftPaidAmt'
CY_BENEFITS = './/{http://www.irs.gov/efile}CYBenefitsPaidToMembersAmt'
PY_BENEFITS = './/{http://www.irs.gov/efile}PYBenefitsPaidToMembersAmt'
TOTAL_ASSETS_BOY = './/{http://www.irs.gov/efile}TotalAssetsBOYAmt'
TOTAL_ASSETS_EOY = './/{http://www.irs.gov/efile}TotalAssetsEOYAmt'
TOTAL_LIABILITIES_BOY = './/{http://www.irs.gov/efile}TotalLiabilitiesBOYAmt'
TOTAL_LIABILITIES_EOY = './/{http://www.irs.gov/efile}TotalLiabilitiesEOYAmt'

# Predefined xml paths for interested elements for 990EZ form
CY_TOTAL_REVENUE_EZ = './/{http://www.irs.gov/efile}TotalRevenueAmt'
CY_CONTRIBUTIONS_EZ = './/{http://www.irs.gov/efile}ContributionsGiftsGrantsEtcAmt'
CY_SERVICE_REV_EZ = './/{http://www.irs.gov/efile}ProgramServiceRevenueAmt'
CY_INVESTMENT_INCOME_EZ = './/{http://www.irs.gov/efile}GrossInvestmentIncome509Grp'
CY_TOTAL_EXPENSES_EZ = './/{http://www.irs.gov/efile}TotalExpensesAmt'
CY_GRANTS_PAID_EZ = './/{http://www.irs.gov/efile}GrantsAndSimilarAmountsPaidAmt'
CY_SALARIES_EZ = './/{http://www.irs.gov/efile}SalariesOtherCompEmplBnftAmt'
CY_BENEFITS_EZ = './/{http://www.irs.gov/efile}BenefitsPaidToOrForMembersAmt'
TOTAL_ASSETS_GRP_EZ = './/{http://www.irs.gov/efile}Form990TotalAssetsGrp'
TOTAL_LIABILITIES_GRP_EZ = './/{http://www.irs.gov/efile}SumOfTotalLiabilitiesGrp'

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
    fields['cy_investment_income'] = get_field_abstract(root, CY_INVESTMENT_INCOME)
    fields['py_investment_income'] = get_field_abstract(root, PY_INVESTMENT_INCOME)
    fields['cy_total_expenses'] = get_field_abstract(root, CY_TOTAL_EXPENSES)
    fields['py_total_expenses'] = get_field_abstract(root, PY_TOTAL_EXPENSES)
    fields['cy_grants_paid'] = get_field_abstract(root, CY_GRANTS_PAID)
    fields['py_grants_paid'] = get_field_abstract(root, PY_GRANTS_PAID)
    fields['cy_salaries'] = get_field_abstract(root, CY_SALARIES)
    fields['py_salaries'] = get_field_abstract(root, PY_SALARIES)
    fields['cy_benefits'] = get_field_abstract(root, CY_BENEFITS)
    fields['py_benefits'] = get_field_abstract(root, PY_BENEFITS)
    fields['total_assets_boy'] = get_field_abstract(root, TOTAL_ASSETS_BOY)
    fields['total_assets_eoy'] = get_field_abstract(root, TOTAL_ASSETS_EOY)
    fields['total_liabilities_boy'] = get_field_abstract(root, TOTAL_LIABILITIES_BOY)
    fields['total_liabilities_eoy'] = get_field_abstract(root, TOTAL_LIABILITIES_EOY)
    return fields

def get_990ez_fields(root):
    fields = defaultdict(lambda: None)
    fields['cy_total_revenue'] = get_field_abstract(root, CY_TOTAL_REVENUE_EZ)
    fields['cy_contributions'] = get_field_abstract(root, CY_CONTRIBUTIONS_EZ)
    fields['cy_service_revenue'] = get_field_abstract(root, CY_SERVICE_REV_EZ)
    fields['cy_investment_income'] = get_field_abstract(root, CY_INVESTMENT_INCOME_EZ)
    fields['cy_total_expenses'] = get_field_abstract(root, CY_TOTAL_EXPENSES_EZ)
    fields['cy_grants_paid'] = get_field_abstract(root, CY_GRANTS_PAID_EZ)
    fields['cy_salaries'] = get_field_abstract(root, CY_SALARIES_EZ)
    fields['cy_benefits'] = get_field_abstract(root, CY_BENEFITS_EZ)
    fields['total_assets_boy'] = try_attribute(root, TOTAL_ASSETS_GRP_EZ, 0)
    fields['total_assets_eoy'] = try_attribute(root, TOTAL_ASSETS_GRP_EZ, 1)
    fields['total_liabilities_boy'] = try_attribute(root, TOTAL_LIABILITIES_GRP_EZ, 0)
    fields['total_liabilities_eoy'] = try_attribute(root, TOTAL_LIABILITIES_GRP_EZ, 1)
    return fields

def get_field_abstract(root, field):
    value = root.find(field)
    return value.text if value is not None else None

def try_attribute(root, field, index):
    try:
        x = root.find(field).getchildren()[index].text
    except Exception:
        x = None
    return x

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