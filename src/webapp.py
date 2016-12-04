from bottle import route, run
from db.dbclient import DBClient

mysql_client = DBClient()

@route('/growth/<key>', method = 'GET')
def get_revenue_growth(key):
    revenue_growth = mysql_client.query_revenue_growth(key)
    if revenue_growth is None:
        return 'There is no organization with electronic id or name %s\n' % key
    else:
        return 'The annual growth of the organization with electronic id or name %s is %s\n' \
               % (key, revenue_growth)

@route('/ranking/<organization_type>/<limit>', method = 'GET')
def get_revenue_growth_ranking(organization_type, limit):
    revenue_growth_ranking = mysql_client.query_by_type(organization_type, int(limit))
    if len(revenue_growth_ranking) == 0:
        return 'There is no organization type %s\n' % organization_type
    else:
        return 'The annual growth ranking of organization type %s is %s\n' \
               % (organization_type, revenue_growth_ranking)

@route('/status', method = 'GET')
def get_status():
    return "It is working!\n"

run(host='0.0.0.0', port=80)
