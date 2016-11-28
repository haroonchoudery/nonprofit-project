import fileparser
from definitions import DATA_DIR
from dbclient import DBClient

data_dict = {
    'index_2016.json' : 'Filings2016.item'
}

if __name__ == "__main__":
    dbclient = DBClient()
    for json_file, prefix in data_dict.items():
        file_path = DATA_DIR + '/' + json_file
        for organization in fileparser.parse_json_index(file_path, prefix):
            print organization.organization_name
            dbclient.insert(organization)
