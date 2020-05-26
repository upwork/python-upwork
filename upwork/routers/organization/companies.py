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


class Api:
    """ """

    client = None

    def __init__(self, client):
        self.client = client

    def get_list(self):
        """Get Companies Info"""
        return self.client.get("/hr/v2/companies")

    def get_specific(self, company_reference):
        """Get Specific Company

        :param company_reference: String

        """
        return self.client.get("/hr/v2/companies/{0}".format(company_reference))

    def get_teams(self, company_reference):
        """Get Teams in Company

        :param company_reference: String

        """
        return self.client.get("/hr/v2/companies/{0}/teams".format(company_reference))

    def get_users(self, company_reference):
        """Get Users in Company

        :param company_reference: String

        """
        return self.client.get("/hr/v2/companies/{0}/users".format(company_reference))
