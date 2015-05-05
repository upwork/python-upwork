# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

from upwork.namespaces import GdsNamespace


class Finreports(GdsNamespace):
    api_url = 'finreports/'
    version = 2

    def get_provider_billings(self, provider_id, query):
        """
        Generate Billing Reports for a Specific Provider.

        *Parameters:*
          :provider_id:   Provider ID

          :query:         The GDS query string

        """
        url = 'providers/{0}/billings'.format(provider_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_provider_teams_billings(self, provider_team_id, query):
        """
        Generate Billing Reports for a Specific Provider's Team.
        The authenticated user must be an admin or
        a staffing manager of the team.

        *Parameters:*
          :provider_team_id:  Provider's Team ID

          :query:             The GDS query string

        """
        url = 'provider_teams/{0}/billings'.format(provider_team_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_provider_companies_billings(self, provider_company_id, query):
        """
        Generate Billing Reports for a Specific Provider's Company.
        The authenticated user must be the company owner

        *Parameters:*
          :provider_company_id:   Provider's Company ID

          :query:                 The GDS query string

        """
        url = 'provider_companies/{0}/billings'.format(provider_company_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_provider_earnings(self, provider_id, query):
        """
        Generate Earning Reports for a Specific Provider

        *Parameters:*
          :provider_id:   Provider ID

          :query:         The GDS query string

        """
        url = 'providers/{0}/earnings'.format(provider_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_provider_teams_earnings(self, provider_team_id, query):
        """
        Generate Earning Reports for a Specific Provider's Team.

        *Parameters:*
          :provider_team_id:  Provider's Team ID

          :query:             The GDS query string

        """
        url = 'provider_teams/{0}/earnings'.format(provider_team_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_provider_companies_earnings(self, provider_company_id, query):
        """
        Generate Earning Reports for a Specific Provider's Company.

        *Parameters:*
          :provider_company_id:   Provider's Team ID

          :query:                 The GDS query string

        """
        url = 'provider_companies/{0}/earnings'.format(provider_company_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_buyer_teams_billings(self, buyer_team_id, query):
        """
        Generate Billing Reports for a Specific Buyer's Team.
        The authenticated user must be an admin or
        a staffing manager of the team.

        *Parameters:*
          :buyer_team_id:     Buyer's Team ID

          :query:             The GDS query string

        """
        url = 'buyer_teams/{0}/billings'.format(buyer_team_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_buyer_companies_billings(self, buyer_company_id, query):
        """
        Generate Billing Reports for a Specific Buyer's Company.
        The authenticated user must be the company owner.

        *Parameters:*
          :buyer_company_id:  Buyer's Company ID

          :query:             The GDS query string
        """
        url = 'buyer_companies/{0}/billings'.format(buyer_company_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_buyer_teams_earnings(self, buyer_team_id, query):
        """
        Generate Earning Reports for a Specific Buyer's Team.

        *Parameters:*
          :buyer_team_id:     Buyer's Team ID

          :query:             The GDS query string

        """
        url = 'buyer_teams/{0}/earnings'.format(buyer_team_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_buyer_companies_earnings(self, buyer_company_id, query):
        """
        Generate Earning Reports for a Specific Buyer's Company.

        *Parameters:*
          :buyer_company_id:  Buyer's Team ID

          :query:             The GDS query string

        """
        url = 'buyer_companies/{0}/earnings'.format(buyer_company_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_financial_entities(self, accounting_id, query):
        """
        Generate Financial Reports for a Specific Account.

        *Parameters:*
          :accounting_id:     ID of an Accounting entity

          :query:             The GDS query string

        """
        url = 'financial_accounts/{0}'.format(accounting_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_financial_entities_provider(self, provider_id, query):
        """
        Generate Financial Reports for an owned Account.

        *Parameters:*
          :provider_id:       Provider ID

          :query:             The GDS query string

        """
        url = 'financial_account_owner/{0}'.format(provider_id)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result
