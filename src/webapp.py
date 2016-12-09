from db.dbclient import DBClient
from flask import Flask
from flask import render_template

mysql_client = DBClient()
app = Flask(__name__)

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/growth?key=<key>', methods = ['GET'])
def get_revenue_growth(key):
    revenue_growth = mysql_client.query_revenue_growth(key)
    if revenue_growth is None:
        return 'There is no organization with electronic id or name %s\n' % key
    else:
        return 'The annual growth of the organization with electronic id or name %s is %s\n' % (key, revenue_growth)

@app.route('/ranking/<organization_type>/<limit>', methods = ['GET'])
def get_revenue_growth_ranking(organization_type, limit):
    revenue_growth_ranking = mysql_client.query_by_type(organization_type, int(limit))
    if len(revenue_growth_ranking) == 0:
        return 'There is no organization type %s\n' % organization_type
    else:
        return 'The annual growth ranking of organization type %s is %s\n' \
               % (organization_type, revenue_growth_ranking)

@app.route('/status', methods = ['GET'])
def get_status():
    return "It is working!\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)