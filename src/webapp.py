from db.dbclient import DBClient
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json

mysql_client = DBClient()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/score', methods = ['POST'])
def get_revenue_growth():
    
    key = request.form['key']
    if key.isdigit():
        key = int(key)
    else:
        key = key

    revenue_growth = mysql_client.query_revenue_growth(key)

    return json.dumps({'status':'OK', 'key':key, 'revenue_growth':revenue_growth});
    # return revenue_growth
    # return render_template('test.html', revenue_growth=revenue_growth)

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