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
