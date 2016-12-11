"""
This module will access the Amazon filings page and populate the database with
interested data.
"""

import parser.jsonparser as jsonparser
from db.dbclient import DBClient

# The number of objects to process in the source index file
LIMIT = 20

# This points to the most recent electronic 990 filing index hosted by Amazon
data_source_dict = {
    'https://s3.amazonaws.com/irs-form-990/index_2016.json' : 'Filings2016.item'
}

if __name__ == "__main__":
    dbclient = DBClient()
    for url, prefix in data_source_dict.items():
        for organization in jsonparser.parse_json_index(url, prefix, LIMIT):
            print organization
            dbclient.upsert(organization)
