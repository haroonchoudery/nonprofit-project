class Organization():

    """This class represents an object of a tax exempt organization"""

    def __init__(self, electronic_id, organization_name, organization_type,
                 current_year_revenue, prior_year_revenue):
        self.electronic_id = int(electronic_id)
        self.organization_name = organization_name
        self.organization_type = organization_type
        self.set_current_year_revenue(current_year_revenue)
        self.set_prior_year_revenue(prior_year_revenue)
        self.set_annual_revenue_growth(current_year_revenue, prior_year_revenue)

    def set_current_year_revenue(self, current_year_revenue):
        if current_year_revenue is not None:
            self.current_year_revenue = int(current_year_revenue)
        else:
            self.current_year_revenue = None

    def set_prior_year_revenue(self, prior_year_revenue):
        if prior_year_revenue is not None:
            self.prior_year_revenue = int(prior_year_revenue)
        else:
            self.prior_year_revenue = None

    def set_annual_revenue_growth(self, current_year_revenue, prior_year_revenue):
        if current_year_revenue is None or \
           prior_year_revenue is None or \
           prior_year_revenue == 0:
           self.annual_revenue_growth = None
        else:
           growth = float(current_year_revenue) / float(prior_year_revenue) - 1
           self.annual_revenue_growth =round(growth, 2)
