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

    def get_workdiary(self, company, date, params={}):
        """Get Workdiary by Company
        
        Parameters:
        :param company:
        :param date:
        :param params:  (Default value = {})

        """
        return self.client.get(
            "/team/v3/workdiaries/companies/{0}/{1}".format(company, date), params
        )

    def get_by_contract(self, contract, date, params={}):
        """Get Work Diary by Contract
        
        Parameters:
        :param contract: 
        :param date: 
        :param params:  (Default value = {})

        """
        return self.client.get(
            "/team/v3/workdiaries/contracts/{0}/{1}".format(contract, date), params
        )
