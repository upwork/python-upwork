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

    def suspend_contract(self, reference, params):
        """Suspend Contract
        
        Parameters:

        :param reference: 
        :param params: 

        """
        return self.client.put("/hr/v2/contracts/{0}/suspend".format(reference), params)

    def restart_contract(self, reference, params):
        """Restart Contract
        
        Parameters:

        :param reference: 
        :param params: 

        """
        return self.client.put("/hr/v2/contracts/{0}/restart".format(reference), params)

    def end_contract(self, reference, params):
        """End Contract
        
        Parameters:

        :param reference: 
        :param params: 

        """
        return self.client.delete("/hr/v2/contracts/{0}".format(reference), params)
