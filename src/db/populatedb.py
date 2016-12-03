import parser.jsonparser as jsonparser
from db.dbclient import DBClient

data_dict = {
    'https://s3.amazonaws.com/irs-form-990/index_2016.json' : 'Filings2016.item'
}

if __name__ == "__main__":
    dbclient = DBClient()
    for url, prefix in data_dict.items():
        for organization in jsonparser.parse_json_index(url, prefix):
            print organization
            dbclient.insert(organization)
