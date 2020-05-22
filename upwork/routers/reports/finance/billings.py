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

    def get_by_freelancer(self, freelancer_reference, params):
        """Generate Billing Reports for a Specific Freelancer
        
        Parameters:

        :param freelancer_reference: 
        :param params: 

        """
        return self.client.get(
            "/finreports/v2/providers/{0}/billings".format(freelancer_reference), params
        )

    def get_by_freelancers_team(self, freelancer_team_reference, params):
        """Generate Billing Reports for a Specific Freelancer's Team
        
        Parameters:

        :param freelancer_team_reference: 
        :param params: 

        """
        return self.client.get(
            "/finreports/v2/provider_teams/{0}/billings".format(
                freelancer_team_reference
            ),
            params,
        )

    def get_by_freelancers_company(self, freelancer_company_reference, params):
        """Generate Billing Reports for a Specific Freelancer's Company
        
        Parameters:

        :param freelancer_company_reference: 
        :param params: 

        """
        return self.client.get(
            "/finreports/v2/provider_companies/{0}/billings".format(
                freelancer_company_reference
            ),
            params,
        )

    def get_by_buyers_team(self, buyer_team_reference, params):
        """Generate Billing Reports for a Specific Buyer's Team
        
        Parameters:

        :param buyer_team_reference: 
        :param params: 

        """
        return self.client.get(
            "/finreports/v2/buyer_teams/{0}/billings".format(buyer_team_reference),
            params,
        )

    def get_by_buyers_company(self, buyer_company_reference, params):
        """Generate Billing Reports for a Specific Buyer's Company
        
        Parameters:

        :param buyer_company_reference: 
        :param params: 

        """
        return self.client.get(
            "/finreports/v2/buyer_companies/{0}/billings".format(
                buyer_company_reference
            ),
            params,
        )
