# Licensed under the Upwork's API Terms of Use;
# you may not use this file except in compliance with the Terms.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author::    Maksym Novozhylov (mnovozhilov@upwork.com)
# Copyright:: Copyright 2020(c) Upwork.com
# License::   See LICENSE.txt and TOS - https://developers.upwork.com/api-tos.html


class Gds:
    """ """

    client = None
    entry_point = "gds"

    def __init__(self, client):
        self.client = client
        self.client.epoint = self.entry_point

    def get_by_team_full(self, company, team, params):
        """Generate Time Reports for a Specific Team (with financial info)
        
        Parameters:

        :param company: 
        :param team: 
        :param params: 

        """
        return self.__get_by_type(company, team, None, params, False)

    def get_by_team_limited(self, company, team, params):
        """Generate Time Reports for a Specific Team (hide financial info)
        
        Parameters:

        :param company: 
        :param team: 
        :param params: 

        """
        return self.__get_by_type(company, team, None, params, True)

    def get_by_agency(self, company, agency, params):
        """Generating Agency Specific Reports
        
        Parameters:

        :param company: 
        :param agency: 
        :param params: 

        """
        return self.__get_by_type(company, None, agency, params, False)

    def get_by_company(self, company, params):
        """Generating Company Wide Reports
        
        Parameters:

        :param company: 
        :param params: 

        """
        return self.__get_by_type(company, None, None, params, False)

    def get_by_freelancer_limited(self, freelancer_id, params):
        """Generating Freelancer's Specific Reports (hide financial info)
        
        Parameters:

        :param freelancer_id: 
        :param params: 

        """
        return self.client.get(
            "/timereports/v1/providers/{0}/hours".format(freelancer_id), params
        )

    def get_by_freelancer_full(self, freelancer_id, params):
        """Generating Freelancer's Specific Reports (with financial info)
        
        Parameters:

        :param freelancer_id: 
        :param params: 

        """
        return self.client.get(
            "/timereports/v1/providers/{0}".format(freelancer_id), params
        )

    def __get_by_type(self, company, team, agency, params, hide_fin_data):
        url = ""
        if team is not None:
            url = "/teams/{0}".format(team)
            if hide_fin_data:
                url = url + "/hours"
        elif agency is not None:
            url = "/agencies/{0}".format(agency)

        return self.client.get(
            "/timereports/v1/companies/{0}{1}".format(company, url), params
        )
