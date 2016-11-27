class Organization():

    """This class represents an object of a tax exempt organization"""

    def __init__(self, electronic_id, organization_name, organization_type,
                 current_year_revenue, prior_year_revenue):
        self.electronic_id = int(electronic_id)
        self.organization_name = organization_name
        self.organization_type = organization_type
        self.current_year_revenue = int(current_year_revenue)
        self.prior_year_revenue = int(prior_year_revenue)
        self.annual_revenue_growth = \
            self.compute_annual_revenue_growth(current_year_revenue,
                                               prior_year_revenue)

    def compute_annual_revenue_growth(self,
                                      current_year_revenue,
                                      prior_year_revenue):
        growth = float(current_year_revenue) / float(prior_year_revenue) - 1
        growth =round(growth, 2)
        return growth
