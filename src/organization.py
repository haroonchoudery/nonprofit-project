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
                              'cy_contributions', 'py_contributions']
        for field_key in numeric_field_keys:
            field = fields[field_key]
            self[field_key] = int(field) if field is not None else None

        # Computation based on the raw input values
        self._set_other_revenue()
        self._set_growth_rate(self['cy_total_revenue'], self['py_total_revenue'],
                             'annual_total_revenue_growth')
        self._set_growth_rate(self['cy_service_revenue'], self['py_service_revenue'],
                             'annual_service_revenue_growth')
        self._set_growth_rate(self['cy_contributions'], self['py_contributions'],
                             'annual_contributions_growth')

    def _set_other_revenue(self):
        if self['cy_total_revenue'] is not None:
            self['cy_other_revenue'] = (self['cy_total_revenue'] - int(self['cy_contributions'] or 0) - 
                                        int(self['cy_service_revenue'] or 0) - int(self['cy_investment_income'] or 0))
        else:
            self['cy_other_revenue'] = None
            
        if self['py_total_revenue'] is not None:
            self['py_other_revenue'] = (self['py_total_revenue'] - int(self['py_contributions'] or 0) - 
                                        int(self['py_service_revenue'] or 0) - int(self['py_investment_income'] or 0))
        else:
            self['py_other_revenue'] = None
    
        # Computation based on the raw input values
        self._set_growth_rate(self['cy_total_revenue'], self['py_total_revenue'],
                             'annual_totoal_revenue_growth')
        self._set_growth_rate(self['cy_service_revenue'], self['py_service_revenue'],
                             'annual_service_revenue_growth')
        self._set_growth_rate(self['cy_contributions'], self['py_contributions'],
                             'annual_contributions_growth')

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
