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

@app.route('/score', methods = ['POST'])
def get_score():

    key = request.form['key']
    if key.isdigit():
        key = int(key)
    else:
        key = key

    score = mysql_client.get_credit_score(key)

    return json.dumps({'status':'OK', 'key':key, 'score':score});

@app.route('/id/<id>', methods = ['GET'])
def get_id(id):
    # This method is for debug only. Should be removed in the final version.
    result = mysql_client.get_credit_score(id)
    return str(result) + '\n'

@app.route('/status', methods = ['GET'])
def get_status():
    return "It is working!\n"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
