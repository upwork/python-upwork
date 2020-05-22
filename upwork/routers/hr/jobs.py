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

    def get_list(self, params):
        """Get list of jobs
        
        Parameters:

        :param params: 

        """
        return self.client.get("/hr/v2/jobs", params)

    def get_specific(self, key):
        """Get specific job by key

        :param key: String

        """
        return self.client.get("/hr/v2/jobs/{0}".format(key))

    def post_job(self, params):
        """Post a new job
        
        Parameters:

        :param params: 

        """
        return self.client.post("/hr/v2/jobs", params)

    def edit_job(self, key, params):
        """Edit existent job
        
        Parameters:

        :param key: 
        :param params: 

        """
        self.client.put("/hr/v2/jobs/{0}".format(key), params)

    def delete_job(self, key, params):
        """Delete existent job
        
        Parameters:

        :param key: 
        :param params: 

        """
        self.client.delete("/hr/v2/jobs/{0}".format(key), params)
