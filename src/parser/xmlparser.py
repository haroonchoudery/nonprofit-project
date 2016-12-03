import urllib2
from lxml import etree

# Paths in the xml tax form
ORGANIZATION_TYPE = "//*[re:test(local-name(), '^Organization.*')]"
CURRENT_YEAR_REVENUE = './/{http://www.irs.gov/efile}CYTotalRevenueAmt'
PRIOR_YEAR_REVENUE = './/{http://www.irs.gov/efile}PYTotalRevenueAmt'

def parse_xml_form(url):
    tree = etree.ElementTree(file=urllib2.urlopen(url))
    root=tree.getroot()

    current_year_revenue = get_current_year_revenue(root)
    prior_year_revenue = get_prior_year_revenue(root)
    organization_type = get_organization_type(root)
    return organization_type, current_year_revenue, prior_year_revenue

def get_current_year_revenue(root):
    current_year_revenue = root.find(CURRENT_YEAR_REVENUE)
    return current_year_revenue.text if current_year_revenue is not None else None

def get_prior_year_revenue(root):
    prior_year_revenue = root.find(PRIOR_YEAR_REVENUE)
    return prior_year_revenue.text if prior_year_revenue is not None else None

def get_organization_type(root):
    organization_tag = root.xpath(ORGANIZATION_TYPE,
                                  namespaces={'re': "http://exslt.org/regular-expressions"})[0].tag
    if organization_tag is None:
        return None
    else:
        organization_type = organization_tag.split('Organization')[1]
        return organization_type
