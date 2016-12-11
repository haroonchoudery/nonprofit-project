import math

class Organization(dict):

    """This class represents an object of a tax exempt organization"""

    def __init__(self, fields):
        # The fields below should be plain text
        text_field_keys = ['form_type', 'organization_name', 'organization_type']
        for field_key in text_field_keys:
            self[field_key] = fields[field_key]

        # The fields below should be integer
        numeric_field_keys = ['electronic_id', 'tax_year', 'cy_total_revenue', 'py_total_revenue',
                              'cy_service_revenue', 'py_service_revenue',
                              'cy_contributions', 'py_contributions',
                              'cy_investment_income', 'py_investment_income',
                              'cy_total_expenses', 'py_total_expenses',
                              'cy_grants_paid', 'py_grants_paid',
                              'cy_salaries', 'py_salaries',
                              'cy_benefits', 'py_benefits',
                              'total_assets_boy', 'total_assets_eoy',
                              'total_liabilities_boy', 'total_liabilities_eoy'
                             ]
        for field_key in numeric_field_keys:
            field = fields[field_key]
            try:
                self[field_key] = int(field) if field is not None else None
            except ValueError:
                self[field_key] = None

        # Computation based on the raw input values
        self._set_other_revenue()
        self._set_other_expenses()
        self._set_revenue_less_expenses()
        self._set_net_assets()
        self._set_growth_rate(self['cy_total_revenue'], self['py_total_revenue'],
                             'annual_total_revenue_growth')
        self._set_growth_rate(self['cy_total_expenses'], self['py_total_expenses'],
                             'annual_total_expenses_growth')
        self._set_growth_rate(self['total_assets_eoy'], self['total_assets_boy'],
                             'annual_total_assets_growth')
        self._set_growth_rate(self['total_liabilities_eoy'], self['total_liabilities_boy'],
                              'annual_total_liabilities_growth')
        self._set_growth_rate(self['net_assets_eoy'], self['net_assets_boy'],
                              'annual_net_assets_growth')
        self._set_ratios()
        self._set_credit_score()

    def _set_other_revenue(self):
        if self['cy_total_revenue'] is not None:
            self['cy_other_revenue'] = (self['cy_total_revenue'] - 
                                        self.sum_fields(['cy_contributions', 'cy_service_revenue', 'cy_investment_income']))
        else:
            self['cy_other_revenue'] = None
            
        if self['py_total_revenue'] is not None:
            self['py_other_revenue'] = (self['py_total_revenue'] -
                                        self.sum_fields(['py_contributions', 'py_service_revenue', 'py_investment_income']))
        else:
            self['py_other_revenue'] = None
            
    def _set_other_expenses(self):
        if self['cy_total_expenses'] is not None:
            self['cy_other_expenses'] = (self['cy_total_expenses'] - 
                                         self.sum_fields(['cy_grants_paid', 'cy_salaries', 'cy_benefits']))
        else:
            self['cy_other_expenses'] = None
        
        if self['py_total_expenses'] is not None:
            self['py_other_expenses'] = (self['cy_total_expenses'] -
                                         self.sum_fields(['py_grants_paid', 'py_salaries', 'py_benefits']))
        else:
            self['py_other_expenses'] = None
        
    def _set_revenue_less_expenses(self):
        if self['cy_total_revenue'] is not None or self['cy_total_expenses'] is not None:
            self['cy_revenue_less_expenses'] = (int(self.int_or_zero(self['cy_total_revenue'])) - 
                                                int(self.int_or_zero(self['cy_total_expenses'])))
        else:
            self['cy_revenue_less_expenses'] = None
            
        if self['py_total_revenue'] is not None or self['py_total_expenses'] is not None:
            self['py_revenue_less_expenses'] = (int(self.int_or_zero(self['py_total_revenue'])) -
                                                int(self.int_or_zero(self['py_total_expenses'])))
        else:
            self['py_revenue_less_expenses'] = None
            
    def _set_net_assets(self):
        self['net_assets_boy'] = self.int_or_zero(self['total_assets_boy']) - self.int_or_zero(self['total_liabilities_boy'])
        self['net_assets_eoy'] = self.int_or_zero(self['total_assets_eoy']) - self.int_or_zero(self['total_liabilities_eoy'])
        
    def _set_ratios(self):
        self['cy_operating_reserve'] = (self['net_assets_eoy'] / self['cy_total_expenses']
                                        if self['cy_total_expenses'] not in [0, None] else None)
        self['cy_operating_efficiency'] = (self['cy_total_revenue'] / self['cy_total_assets']
                                           if self['cy_total_revenue'] is not None
                                           and (self['cy_total_assets'] not in [0, None]
                                                and self['cy_total_assets'] > 0) else None)
        self['cy_net_margin'] = (self['cy_revenue_less_expenses'] / self['cy_total_revenue']
                                 if self['cy_revenue_less_expenses'] is not None
                                 and (self['cy_total_revenue'] not in [0, None]
                                      and self['cy_total_revenue'] > 0) else None)
        self['cy_leverage_efficiency'] = (self['cy_total_revenue'] / self['net_assets_eoy']
                                          if self['cy_total_revenue'] is not None
                                          and (self['net_assets_eoy'] not in [0, None]
                                               and self['net_assets_eoy'] > 0) else None)
        self['cy_debt_ratio'] = (self['total_liabilities_eoy'] / self['total_assets_eoy']
                                 if self['total_liabilities_eoy'] is not None
                                 and (self['total_assets_eoy'] not in [0, None]
                                      and self['total_assets_eoy'] > 0) else None)
        self['cy_financial_leverage'] = (self['total_liabilities_eoy'] / self['net_assets_eoy']
                                         if self['total_liabilities_eoy'] is not None
                                         and (self['net_assets_eoy'] not in [0, None]
                                              and self['net_assets_eoy'] > 0) else None)
        
    def _set_credit_score(self):
        cs = 0
        cs += min(max(self.float_or_zero(self['cy_operating_reserve']) * 0.4, -2), 2)
        cs += min(max(self.float_or_zero(self['annual_net_assets_growth']) * 20, -2), 2)
        cs += min(max(self.float_or_zero(self['cy_operating_efficiency']), -2), 2)
        cs += min(max(self.float_or_zero(self['cy_revenue_less_expenses']) * 20, -2), 2)
        cs += min(max(self.float_or_zero(self['annual_total_assets_growth']) * 20, -2), 2)
        cs += min(max(self.float_or_zero(self['cy_leverage_efficiency']), -2), 2)
        cs += min(max(self.float_or_zero(self['cy_debt_ratio']) * -4 + 2, -2), 2)
        cs += min(max(self.float_or_zero(self['cy_financial_leverage']) * -1 + 2, -2), 2)
        if self['annual_total_revenue_growth'] is not None and self['annual_total_expense_growth'] is not None:
            if self['annual_total_revenue_growth'] > self['annual_total_expense_growth']:
                cs += 0.5
            elif self['annual_total_revenue_growth'] < self['annual_total_expense_growth']:
                cs -= 0.5
        score = 300 + 550 / (1 + math.exp(-0.2 * cs))
        if cs == 0:
            self['cy_credit_score'] = None
        else:
            self['cy_credit_score'] = int(score)
                    
    def __missing__(self, key):
        return None

    def _set_growth_rate(self, cy_data, py_data, field_key):
        """This method will compute the annual growth for a given numeric field
        based on the current year value and the prior year value.
        """
        if cy_data is None or py_data is None or int(py_data) == 0:
            self[field_key] = None
        else:
            growth = (float(cy_data) - float(py_data)) / float(py_data)
            self[field_key] = round(growth, 2)
        pass

    def sum_fields(self, fields):
        total = 0
        for field in fields:
            total += self.int_or_zero(self[field])
        return total
                    
    @staticmethod
    def int_or_zero(x):
        return int(x or 0)
    
    @staticmethod
    def float_or_zero(x):
        return float(x or 0)