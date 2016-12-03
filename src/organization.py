class Organization(dict):

    """This class represents an object of a tax exempt organization"""

    #def __init__(self, electronic_id, tax_year, form_type, organization_name, organization_type,
    #             current_year_revenue, prior_year_revenue):
    def __init__(self, fields):
        fieldNames = ['tax_year', 'form_type', 'organization_name', 'organization_type']
        self['electronic_id'] = int(fields['electronic_id'])
        for f in fieldNames:
            self[f] = fields[f]
        self.set_current_year_revenue(fields['cy_total_revenue'])
        self.set_prior_year_revenue(fields['py_total_revenue'])
        self.set_annual_revenue_growth(self['cy_total_revenue'], self['py_total_revenue'])
        
    def __missing__(self, key):
        return None

    def set_current_year_revenue(self, current_year_revenue):
        if current_year_revenue is not None:
            self['cy_total_revenue'] = int(current_year_revenue)
        else:
            self['cy_total_revenue'] = None

    def set_prior_year_revenue(self, prior_year_revenue):
        if prior_year_revenue is not None:
            self['py_total_revenue'] = int(prior_year_revenue)
        else:
            self['py_total_revenue'] = None

    def set_annual_revenue_growth(self, current_year_revenue, prior_year_revenue):
        if current_year_revenue is None or \
           prior_year_revenue is None or \
           int(prior_year_revenue) == 0:
           self['annual_revenue_growth'] = None
        else:
           growth = float(current_year_revenue) / float(prior_year_revenue) - 1
           self['annual_revenue_growth'] = round(growth, 2)
