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

    def get_list(self, params={}):
        """Get list of offers
        
        Parameters:

        :param params:  (Default value = {})

        """
        return self.client.get("/offers/v1/contractors/offers", params)

    def get_specific(self, reference):
        """Get specific offer

        :param reference: String

        """
        return self.client.get("/offers/v1/contractors/offers/{0}".format(reference))

    def actions(self, reference, params):
        """Make an Offer
        
        Parameters:

        :param reference: 
        :param params: 

        """
        return self.client.post(
            "/offers/v1/contractors/actions/{0}".format(reference), params
        )
