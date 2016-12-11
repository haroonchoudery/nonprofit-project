import sys
import os
import logging
from logging import config
from functools import wraps
from mysql.connector.pooling import MySQLConnectionPool

DATABASE = 'organizations'
DML_TABLE = 'tax_exempt_organizations'
VIEW = 'tax_exempt_organizations_current'
USER = 'root'
PASSWORD = ''
HOST = 'localhost'
COLUMNS = (
          '(electronic_id, tax_year, form_type, organization_name, organization_type, ' \
          'cy_total_revenue, py_total_revenue, cy_service_revenue, py_service_revenue, cy_contributions, ' \
          'py_contributions, cy_investment_income, py_investment_income, cy_total_expenses, ' \
          'py_total_expenses, cy_grants_paid, py_grants_paid, cy_salaries, py_salaries, ' \
          'cy_benefits, py_benefits, total_assets_boy, total_assets_eoy, ' \
          'total_liabilities_boy, total_liabilities_eoy, net_assets_boy, net_assets_eoy, ' \
          'annual_total_revenue_growth, annual_total_expenses_growth, annual_total_assets_growth, ' \
          'annual_total_liabilities_growth, annual_net_assets_growth, cy_operating_reserve, ' \
          'cy_operating_efficiency, cy_net_margin, cy_leverage_efficiency, cy_debt_ratio, ' \
          'cy_financial_leverage, cy_credit_score)'
          )

class DBClient(object):

    """The client class to interact with the mysql database"""

    dbconfig = {
        'host': HOST,
        'database': DATABASE,
        'user': USER,
        'password': PASSWORD
    }

    config_file = os.path.join(os.environ['CONFROOT'], 'log.conf')
    logging.config.fileConfig(config_file)

    def __init__(self):
        dbconfig = DBClient.dbconfig
        self.cnxpool = MySQLConnectionPool(pool_reset_session=False, **dbconfig)
        self.logger = logging.getLogger('DB')


    def upsert(self, org):
        """Insert an existing item if it doesn't exist, update it otherwise."""
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            delete_existing_record = 'DELETE FROM ' + DML_TABLE + ' WHERE ELECTRONIC_ID = %s AND TAX_YEAR = %s'
            insert_new_organization = 'INSERT INTO ' + DML_TABLE + COLUMNS + \
                                      ' VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' + \
                                      ' %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,' + \
                                      ' %s, %s, %s, %s, %s, %s, %s)'
            cursor.execute(delete_existing_record, (org['electronic_id'],org['tax_year']))
            cursor.execute(insert_new_organization,
                           (org['electronic_id'],
                            org['tax_year'],
                            org['form_type'],
                            org['organization_name'],
                            org['organization_type'],
                            org['cy_total_revenue'],
                            org['py_total_revenue'],
                            org['cy_service_revenue'],
                            org['py_service_revenue'],
                            org['cy_contributions'],
                            org['py_contributions'],
                            org['cy_investment_income'],
                            org['py_investment_income'],
                            org['cy_total_expenses'],
                            org['py_total_expenses'],
                            org['cy_grants_paid'],
                            org['py_grants_paid'],
                            org['cy_salaries'],
                            org['py_salaries'],
                            org['cy_benefits'],
                            org['py_benefits'],
                            org['total_assets_boy'],
                            org['total_assets_eoy'],
                            org['total_liabilities_boy'],
                            org['total_liabilities_eoy'],
                            org['net_assets_boy'],
                            org['net_assets_eoy'],
                            org['annual_total_revenue_growth'],
                            org['annual_total_expenses_growth'],
                            org['annual_total_assets_growth'],
                            org['annual_total_liabilities_growth'],
                            org['annual_net_assets_growth'],
                            org['cy_operating_reserve'],
                            org['cy_operating_efficiency'],
                            org['cy_net_margin'],
                            org['cy_leverage_efficiency'],
                            org['cy_debt_ratio'],
                            org['cy_financial_leverage'],
                            org['cy_credit_score'],
                           )
                          )
            cnx.commit()
        except Exception, error:
            self.logger.error('Fail to upsert organization %s', org['electronic_id'])
            self.logger.exception(error)
        finally:
            cursor.close()
            cnx.close()

    def query_by_id(self, electronic_id):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            query = 'SELECT * FROM ' + VIEW + \
                    ' WHERE electronic_id = %s'
            cursor.execute(query, (electronic_id,))
            result = cursor.fetchall()
            if result is None or len(result) == 0:
                return None
            else:
                return result[0]
        except Exception, error:
            self.logger.error('Fail to query organization %s', org['electronic_id'])
            self.logger.exception(error)
        finally:
            cursor.close()
            cnx.close()

    def query_by_name(self, organization_name):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            query = 'SELECT * FROM ' + VIEW + \
                    ' WHERE organization_name = %s'
            cursor.execute(query, (organization_name,))
            result = cursor.fetchall()
            if result is None or len(result) == 0:
                return None
            else:
                return result[0]
        except Exception, error:
            self.logger.error('Fail to query organization %s', org['electronic_id'])
            self.logger.exception(error)
        finally:
            cursor.close()
            cnx.close()

    def query_by_type(self, organization_type, limit):
        cnx = self.cnxpool.get_connection()
        cursor = cnx.cursor()
        try:
            query = 'SELECT * FROM ' + VIEW + \
                    ' WHERE organization_type = %s ORDER BY annual_total_revenue_growth DESC LIMIT %s'
            cursor.execute(query, (organization_type, limit))
            result = cursor.fetchall()
            return result
        except Exception, error:
            print error
        finally:
            cursor.close()
            cnx.close()

    def get_significant_fields(self, key):
        """Return the significant fields for the credit report."""
        id_result = self.query_by_id(key)
        if id_result is None or len(id_result) == 0:
            return None

        name = id_result[3]
        credit_score = 'Unavailable' if id_result[38] is None else id_result[38]
        total_assets = 'Unavailable' if id_result[22] is None else id_result[22]
        total_revenues = 'Unavailable' if id_result[5] is None else id_result[5]
        net_assests = 'Unavailable' if id_result[26] is None else id_result[26]
        return name, credit_score, total_assets, total_revenues, net_assests
