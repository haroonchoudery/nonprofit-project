import ijson
import urllib2
import xmlparser
from organization import Organization
from collections import defaultdict

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
    objects_990 = (obj for obj in objects if obj[FORM_TYPE] in ['990','990EZ'])
    for obj in objects_990:
        if i == LIMIT:
            break
        else:
            i += 1
            fieldsDict = xmlparser.parse_xml_form(obj[URL], obj[FORM_TYPE])
            fieldsDict['electronic_id'] = obj[ELECTRONIC_ID]
            fieldsDict['form_type'] = obj[FORM_TYPE]
            fieldsDict['organization_name'] = obj[ORGANIZATION_NAME]
            org = Organization(fieldsDict)
            if (org['electronic_id'] is not None
                and org['tax_year'] is not None
                and org['form_type'] is not None):
                    yield org
            else:
                continue