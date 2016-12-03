import pymysql.cursors

DATABASE = 'organizations'
TABLE = 'tax_exempt_organizations'
USER = 'root'
PASSWORD = ''
HOST = 'localhost'
COLUMNS = '(electronic_id, organization_name, organization_type, ' \
          'current_year_revenue, prior_year_revenue, annual_revenue_growth)'

class DBClient():

    """The client class to interact with the mysql database"""

    def get_connection(self):
        return pymysql.connect(user=USER,
                               password=PASSWORD,
                               host=HOST,
                               db=DATABASE)

    def insert(self, org):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                insert_new_organization = 'INSERT INTO ' + TABLE + COLUMNS + \
                                          ' VALUES (%s, %s, %s, %s, %s, %s)'
                cursor.execute(insert_new_organization,
                               (org.electronic_id,
                                org.organization_name,
                                org.organization_type,
                                org.current_year_revenue,
                                org.prior_year_revenue,
                                org.annual_revenue_growth))
                conn.commit()
        finally:
            conn.close()

    def query_by_id(self, electronic_id):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                query = 'SELECT annual_revenue_growth FROM ' + TABLE + \
                        ' WHERE electronic_id = %s'
                cursor.execute(query, (electronic_id))
                result = cursor.fetchone()
                return result
        finally:
            conn.close()

    def query_by_name(self, organization_name):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                query = 'SELECT annual_revenue_growth FROM ' + TABLE + \
                        ' WHERE organization_name = %s'
                cursor.execute(query, (organization_name))
                result = cursor.fetchone()
                return result
        finally:
            conn.close()

    def query_by_type(self, organization_type, limit):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                query = 'SELECT organization_name, annual_revenue_growth FROM ' + \
                TABLE + ' WHERE organization_type = %s ORDER BY annual_revenue_growth DESC LIMIT %s'
                cursor.execute(query, (organization_type, limit))
                result = cursor.fetchall()
                return result
        finally:
            conn.close()

    def query_revenue_growth(self, key):
        id_result = self.query_by_id(key)
        if id_result:
            return id_result[0]

        name_result = self.query_by_name(key)
        if name_result:
            return name_result[0]

        return None
