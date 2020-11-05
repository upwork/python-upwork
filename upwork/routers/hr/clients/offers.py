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
        """
        Initialize the client.

        Args:
            self: (todo): write your description
            client: (todo): write your description
        """
        self.client = client

    def get_list(self, params):
        """Get list of offers
        
        Parameters:

        :param params: 

        """
        return self.client.get("/offers/v1/clients/offers", params)

    def get_specific(self, reference, params):
        """Get specific offer
        
        Parameters:

        :param reference: 
        :param params: 

        """
        return self.client.get(
            "/offers/v1/clients/offers/{0}".format(reference), params
        )

    def make_offer(self, params):
        """Make an Offer
        
        Parameters:

        :param params: 

        """
        return self.client.post("/offers/v1/clients/offers", params)
