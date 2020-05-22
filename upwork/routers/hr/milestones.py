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

    def get_active_milestone(self, contract_id):
        """Get active Milestone for specific Contract

        :param contract_id: String

        """
        return self.client.get(
            "/hr/v3/fp/milestones/statuses/active/contracts/{0}".format(contract_id)
        )

    def get_submissions(self, milestone_id):
        """Get active Milestone for specific Contract

        :param milestone_id: String

        """
        return self.client.get(
            "/hr/v3/fp/milestones/{0}/submissions".format(milestone_id)
        )

    def create(self, params):
        """Create a new Milestone
        
        Parameters:

        :param params: 

        """
        return self.client.post("/hr/v3/fp/milestones", params)

    def edit(self, milestone_id, params):
        """Edit an existing Milestone
        
        Parameters:

        :param milestone_id: 
        :param params: 

        """
        return self.client.put("/hr/v3/fp/milestones/{0}".format(milestone_id), params)

    def activate(self, milestone_id, params):
        """Activate an existing Milestone
        
        Parameters:

        :param milestone_id: 
        :param params: 

        """
        return self.client.put(
            "/hr/v3/fp/milestones/{0}/activate".format(milestone_id), params
        )

    def approve(self, milestone_id, params):
        """Approve an existing Milestone
        
        Parameters:

        :param milestone_id: 
        :param params: 

        """
        return self.client.put(
            "/hr/v3/fp/milestones/{0}/approve".format(milestone_id), params
        )

    def delete(self, milestone_id):
        """Delete an existing Milestone

        :param milestone_id: String

        """
        return self.client.delete("/hr/v3/fp/milestones/{0}".format(milestone_id))
