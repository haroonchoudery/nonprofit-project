import math

class Organization(dict):

    """This class is an abstraction of a real life tax exempt organization.
       It contains the utility to process the raw data extracted from a 990 tax
       form, and computes a credit score based on the raw data.
    """

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
        self._set_growth_rate()
        self._set_ratios()
        self._set_credit_score()

    def _set_growth_rate(self):
        self._compute_growth_rate(self['cy_total_revenue'], self['py_total_revenue'],
                                  'annual_total_revenue_growth')
        self._compute_growth_rate(self['cy_total_expenses'], self['py_total_expenses'],
                                  'annual_total_expenses_growth')
        self._compute_growth_rate(self['total_assets_eoy'], self['total_assets_boy'],
                                  'annual_total_assets_growth')
        self._compute_growth_rate(self['total_liabilities_eoy'], self['total_liabilities_boy'],
                                  'annual_total_liabilities_growth')
        self._compute_growth_rate(self['net_assets_eoy'], self['net_assets_boy'],
                                  'annual_net_assets_growth')

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

        """
        We generate a raw score equal to the sum of 8 financial ratio scores, each in the range [-2, 2].
        There is an additional +/- 0.5 raw score modifier depending on whether revenue growth was
        higher/lower than expense growth respectively (only applies to Form 990, not 990EZ).
        The coefficients for the ratios were determined by sampling 2,000 forms to get a sense of
        the distribution of each ratio. In general, the [-2, 2] ratio score should be ~1 on average
        and only negative for clearly bad results (e.g., negative asset growth, very high debt, etc.)
        If the sum across all ratios is exactly 0, we assume the form did not have sufficient information,
        so we do not assign a credit score. Otherwise, we accept the raw score and convert it to a credit score
        (if some fields are missing, that ratio score will be 0). There is roughly a 10% incidence rate of
        missing credit scores.

        The 8 ratios are:
        Operating reserve = (Net assets) / (Total expenses)
        Growth in net assets = (Ending net assets - Beginning net assets) / (Beginning net assets) - 1
        Operating efficiency = (Total revenue) / (Total assets)
        Net margin = (Total revenue - Total expenses) / (Total revenue)
        Growth in total assets = (Ending total assets - Beginning total assets) / (Beginning total assets) - 1
        Leverage efficiency = (Total revenue) / (Net assets)
        Debt ratio = (Total liabilities) / (Total assets)
        Financial leverage = (Total liabilities) / (Net assets)

        The conversion from raw score to credit score is a logistic function with a slope coefficient of 0.25.
        The credit score ranges from 300 to 850 to look like a FICO score, and it has a similar distribution
        to personal FICO scores (a sample of 900 nonprofit organizations yielded an average score of 703
        with a range of [392, 816] and standard deviation of 106).
        """

        cs = 0
        cs += min(max(self.float_or_zero(self['cy_operating_reserve']) * 0.4, -2), 2)
        cs += min(max(self.float_or_zero(self['annual_net_assets_growth']) * 20, -2), 2)
        cs += min(max(self.float_or_zero(self['cy_operating_efficiency']), -2), 2)
        cs += min(max(self.float_or_zero(self['cy_net_margin']) * 20, -2), 2)
        cs += min(max(self.float_or_zero(self['annual_total_assets_growth']) * 20, -2), 2)
        cs += min(max(self.float_or_zero(self['cy_leverage_efficiency']), -2), 2)
        cs += min(max(self.float_or_zero(self['cy_debt_ratio']) * -4 + 2, -2), 2)
        cs += min(max(self.float_or_zero(self['cy_financial_leverage']) * -1 + 2, -2), 2)
        if self['annual_total_revenue_growth'] is not None and self['annual_total_expense_growth'] is not None:
            if self['annual_total_revenue_growth'] > self['annual_total_expense_growth']:
                cs += 0.5
            elif self['annual_total_revenue_growth'] < self['annual_total_expense_growth']:
                cs -= 0.5
        score = 300 + 550 / (1 + math.exp(-0.25 * cs))
        if cs == 0:
            self['cy_credit_score'] = None
        else:
            self['cy_credit_score'] = int(score)

    def __missing__(self, key):
        return None

    def _compute_growth_rate(self, cy_data, py_data, field_key):
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
