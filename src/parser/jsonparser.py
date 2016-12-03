import ijson
import urllib2
import xmlparser
from organization import Organization

# The number of objects to process in the source index file
LIMIT = 10

# Keys in the json index
ORGANIZATION_NAME = 'OrganizationName'
ELECTRONIC_ID = 'EIN'
URL = 'URL'
FORM_TYPE = 'FormType'

def parse_json_index(url, prefix):
    """This function will parse the given url as json."""

    index = urllib2.urlopen(url)
    objects = ijson.items(index, prefix)

    i = 0
    objects_990 = (obj for obj in objects if obj[FORM_TYPE] == '990')
    for obj in objects_990:
        if i == LIMIT:
            break
        else:
            i += 1
            org_type, current_year_revenue, prior_year_revenue = \
                xmlparser.parse_xml_form(obj[URL])
            org = Organization(obj[ELECTRONIC_ID],
                               obj[ORGANIZATION_NAME],
                               org_type,
                               current_year_revenue,
                               prior_year_revenue)
            yield org
