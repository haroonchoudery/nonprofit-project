from functools import wraps
from mysql.connector.pooling import MySQLConnectionPool

DATABASE = 'organizations'
TABLE = 'tax_exempt_organizations'
USER = 'root'
PASSWORD = ''
HOST = 'localhost'
COLUMNS = '(electronic_id, form_type, organization_name, organization_type, ' \
          'cy_total_revenue, py_total_revenue, cy_service_revenue, py_service_revenue, '\
          'cy_contributions, py_contributions, annual_totoal_revenue_growth, '\
          'annual_service_revenue_growth, annual_contributions_growth)'

class DBClient(object):

    """The client class to interact with the mysql database"""

    dbconfig = {
        'host': HOST,
        'database': DATABASE,
        'user': USER,
        'password': PASSWORD
    }

    def __init__(self):
        dbconfig = DBClient.dbconfig
        self.cnxpool = MySQLConnectionPool(pool_reset_session=False, **dbconfig)

    def upsert(self, org):
        """ Insert an existing item if it doesn't exist, update it otherwise."""
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            delete_existing_record = 'DELETE FROM ' + TABLE + ' WHERE ELECTRONIC_ID = %s'
            insert_new_organization = 'INSERT INTO ' + TABLE + COLUMNS + \
                                      ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(delete_existing_record, (org['electronic_id'],))
            cursor.execute(insert_new_organization,
                           (org['electronic_id'],
                            org['form_type'],
                            org['organization_name'],
                            org['organization_type'],
                            org['cy_total_revenue'],
                            org['py_total_revenue'],
                            org['cy_service_revenue'],
                            org['py_service_revenue'],
                            org['cy_contributions'],
                            org['py_contributions'],
                            org['annual_totoal_revenue_growth'],
                            org['annual_service_revenue_growth'],
                            org['annual_contributions_growth']))
            cnx.commit()
        except Exception, error:
            print error
        finally:
            cursor.close()
            cnx.close()

    def query_by_id(self, electronic_id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            with self.conn.cursor() as cursor:
                query = 'SELECT * FROM ' + TABLE + \
                        ' WHERE electronic_id = %s'
                cursor.execute(query, (electronic_id))
                result = cursor.fetchall()[0]
                return result
        except Exception, error:
            print error
        finally:
            cursor.close()
            cnx.close()

    def query_by_name(self, organization_name):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            with self.conn.cursor() as cursor:
                query = 'SELECT * FROM ' + TABLE + \
                        ' WHERE organization_name = %s'
                cursor.execute(query, (organization_name))
                result = cursor.fetchone()[0]
                return result
        except Exception, error:
            print error
        finally:
            cursor.close()
            cnx.close()

    def query_by_type(self, organization_type, limit):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            with self.conn.cursor() as cursor:
                query = 'SELECT * FROM ' + TABLE + \
                        ' WHERE organization_type = %s ORDER BY annual_totoal_revenue_growth DESC LIMIT %s'
                cursor.execute(query, (organization_type, limit))
                result = cursor.fetchall()
                return result
        except Exception, error:
            print error
        finally:
            cursor.close()
            cnx.close()

    def query_revenue_growth(self, key):
        id_result = self.query_by_id(key)
        if id_result:
            return id_result[10]

        name_result = self.query_by_name(key)
        if name_result:
            return name_result[10]

        return None
