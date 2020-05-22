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

    def get_owned(self, freelancer_reference, params):
        """Generate Financial Reports for an owned Account
        
        Arguments:

        :param freelancer_reference: param params:
        :param params: 

        """
        return self.client.get(
            "/finreports/v2/financial_account_owner/{0}".format(freelancer_reference),
            params,
        )

    def get_specific(self, entity_reference, params):
        """Generate Financial Reports for a Specific Account
        
        Arguments:

        :param entity_reference: param params:
        :param params: 

        """
        return self.client.get(
            "/finreports/v2/financial_accounts/{0}".format(entity_reference), params
        )
