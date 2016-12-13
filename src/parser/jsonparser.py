"""
This module provides the functionalities to process the index file of non profit
electronic IRS filings. The filings index is host by Amazon and exposed to the
public as a JSON page. We will only process filings in 990 and 990EZ form. These
will cover non profits with annual gross receipts larger than 50,000. A detailed
explanation of the index can be found here:
https://aws.amazon.com/public-datasets/irs-990/
"""

import ijson
import urllib2
import xmlparser
from organization import Organization
from collections import defaultdict

# Keys in the json index page to process
ORGANIZATION_NAME = 'OrganizationName'
ELECTRONIC_ID = 'EIN'
URL = 'URL'
FORM_TYPE = 'FormType'

def parse_json_index(url, prefix, limit):
    """This function will parse the given url as json."""

    index = urllib2.urlopen(url)
    objects = ijson.items(index, prefix)

    counter = 0

    filings = (obj for obj in objects if obj[FORM_TYPE] in ['990','990EZ'])
    for filing in filings:
        if counter == limit:
            break
        else:
            counter += 1
            field_dict = xmlparser.parse_xml_form(filing[URL], filing[FORM_TYPE])
            field_dict['electronic_id'] = filing[ELECTRONIC_ID]
            field_dict['form_type'] = filing[FORM_TYPE]
            field_dict['organization_name'] = filing[ORGANIZATION_NAME]
            org = Organization(field_dict)
            if (org['electronic_id'] is not None and
                org['form_type'] is not None):
                    yield org
            else:
                continue
