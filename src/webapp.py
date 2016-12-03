from bottle import route, run
from dbclient import DBClient

mysql_client = DBClient()

@route('/eid/<eid>')
def get_revenue_growth_by_id(eid):
    revenue_growth = mysql_client.query_revenue_growth_by_id(eid)
    if revenue_growth is None:
        return 'There is no organization with electronic id %s' % eid
    else:
        return 'The annual growth of the organization with electronic id %s is %s' \
               % (eid, revenue_growth)

run(host='0.0.0.0', port=80)
