"""
This module will access the Amazon filings page and populate the database with
interested data.
"""

import parser.jsonparser as jsonparser
from heapq import heappush, heappop
from db.dbclient import DBClient

# The number of objects to process in the source index file
LIMIT = 500

# This points to the most recent electronic 990 filing index hosted by Amazon
DATA_SOURCE = {
    'https://s3.amazonaws.com/irs-form-990/index_2016.json' : 'Filings2016.item'
}

def set_score_percentile(org_grouped_by_type):
    """This function computes the score percentile of each organization within
       its own group, and store it into the database. For organization whose credit
       score is unavailable, its percentile will be Null. The computation will only
       be done among organization will valid score.
    """
    dbclient = DBClient()
    for orgs_queue in org_grouped_by_type.values():
        total_count = len(orgs_queue)
        index = 1
        while len(orgs_queue) != 0:
            score, electronic_id = heappop(orgs_queue)
            percentile = round(float(index) / total_count, 2)
            index += 1
            dbclient.update_score_percentile(percentile, electronic_id)

def scan_source_data(source):
    """This function scan the the nonprofit data source and store interested data
       into the database.
    """
    dbclient = DBClient()
    # This dict stores the credit score of each non profit organization, grouped by organization type.
    org_grouped_by_type = {}

    for url, prefix in source.items():
        for org in jsonparser.parse_json_index(url, prefix, LIMIT):
            dbclient.upsert(org)

            # We only care about organization with valid score here.
            if org['cy_credit_score'] is not None:
                # If an organization type is encountered for the first time, create a list for it.
                if org['organization_type'] not in org_grouped_by_type:
                    org_grouped_by_type[org['organization_type']] = []
                # Use priority queue to store the score, id tuple so that we can always keep it in order.
                priority_queue = org_grouped_by_type[org['organization_type']]
                heappush(priority_queue, (org['cy_credit_score'], org['electronic_id']))

    set_score_percentile(org_grouped_by_type)

if __name__ == "__main__":
    scan_source_data(DATA_SOURCE)
