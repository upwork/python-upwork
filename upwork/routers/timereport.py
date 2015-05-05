# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

from upwork.namespaces import GdsNamespace


class TimeReport(GdsNamespace):
    api_url = 'timereports/'
    version = 1

    def get_provider_report(self, provider_id, query, hours=False):
        """
        Get caller's specific time report.

        The caller of this API must be the provider himself.

        *Parameters:*
          :provider_id:   The provider_id of the caller

          :query:         The GDS query string

          :hours:         (optional) Limits the query to hour specific elements
                          and hides all financial details
                          Default: ``False``
        """
        url = 'providers/{0}'.format(provider_id)
        if hours:
            url = '{0}/hours'.format(url)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_company_report(self, company_id, query, hours=False):
        """
        Generate company wide time reports.

        All reporting fields available except earnings related fields.
        In order to access this API the authorized user needs either hiring
        or finance permissions to all teams within the company.

        *Parameters:*
          :company_id:    Company ID

          :query:         The GDS query string

          :hours:         (optional) Limits the query to hour specific elements
                          and hides all financial details
                          Default: ``False``

        """
        url = 'companies/{0}'.format(company_id)
        if hours:
            url = '{0}/hours'.format(url)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_team_report(self, company_id, team_id, query, hours=False):
        """
        Generate team specific time reports.

        *Parameters:*
          :company_id:    The Company ID

          :team_id:       The Team ID

          :query:         The GDS query string

          :hours:         (optional) Limits the query to hour specific elements
                          and hides all financial details
                          Default: ``False``

        """
        url = 'companies/{0}/teams/{1}'.format(company_id, team_id)
        if hours:
            url = '{0}/hours'.format(url)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result

    def get_agency_report(self, company_id, agency_id, query, hours=False):
        """
        Generate agency specific time reports.

        *Parameters:*
          :company_id:    The Company ID

          :agency_id:     The Agency ID

          :query:         The GDS query string

          :hours:         (optional) Limits the query to hour specific elements
                          and hides all financial details
                          Default: ``False``

        """
        url = 'companies/{0}/agencies/{1}'.format(company_id, agency_id)
        if hours:
            url = '{0}/hours'.format(url)
        tq = str(query)
        result = self.get(url, data={'tq': tq})
        return result
