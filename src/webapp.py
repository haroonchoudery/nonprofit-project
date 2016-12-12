import logging
import json
from db.dbclient import DBClient
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

mysql_client = DBClient()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/score', methods = ['POST'])
def get_score():
    key = request.form['key']
    if key.isdigit():
        key = int(key)
    else:
        key = key

    results = mysql_client.query_by_key_metrics(key)
    if results is None:
        return json.dumps({'status':'OK', 'key':key, 'name':None})
    else:
        name, credit_score, total_assets, total_revenues, net_assets, \
        organization_type, tax_year, score_percentile = results
        if score_percentile != 'Unavailable':
            score_percentile = '{0:.0%}'.format(score_percentile)
        return json.dumps({'status':'OK',
                           'key':key,
                           'name': name,
                           'score':credit_score,
                           'total_assets':total_assets,
                           'total_revenues':total_revenues,
                           'net_assets':net_assets,
                           'tax_status': organization_type,
                           'tax_year': tax_year,
                           'score_percentile': score_percentile})

@app.route('/status', methods = ['GET'])
def get_status():
    return "It is working!\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
