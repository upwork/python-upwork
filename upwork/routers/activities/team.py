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

    def get_list(self, company, team):
        """List all oTask/Activity records within a team

        :param company: String
        :param team: String

        """
        return self.__get_by_type(company, team)

    def get_specific_list(self, company, team, code):
        """List all oTask/Activity records within a Company by specified code(s)

        :param company: String
        :param team: String
        :param code: String

        """
        return self.__get_by_type(company, team, code)

    def add_activity(self, company, team, params):
        """Create an oTask/Activity record within a team
        
        Parameters:
        :param company: 
        :param team: 
        :param params: 

        """
        return self.client.post(
            "/otask/v1/tasks/companies/{0}/teams/{1}/tasks".format(company, team),
            params,
        )

    def update_activities(self, company, team, code, params):
        """Update specific oTask/Activity record within a team
        
        Parameters:
        :param company: 
        :param team: 
        :param code: 
        :param params: 

        """
        return self.client.put(
            "/otask/v1/tasks/companies/{0}/teams/{1}/tasks/{2}".format(
                company, team, code
            ),
            params,
        )

    def archive_activities(self, company, team, code):
        """Archive specific oTask/Activity record within a team

        :param company: String
        :param team: String
        :param code: String

        """
        return self.client.put(
            "/otask/v1/tasks/companies/{0}/teams/{1}/archive/{2}".format(
                company, team, code
            )
        )

    def unarchive_activities(self, company, team, code):
        """Unarchive specific oTask/Activity record within a team

        :param company: String
        :param team: String
        :param code: String

        """
        return self.client.put(
            "/otask/v1/tasks/companies/{0}/teams/{1}/unarchive/{2}".format(
                company, team, code
            )
        )

    def update_batch(self, company, params):
        """Update a group of oTask/Activity records within a company
        
        Parameters:
        :param company: 
        :param params: 

        """
        return self.client.put(
            "/otask/v1/tasks/companies/{0}/tasks/batch".format(company), params
        )

    def __get_by_type(self, company, team, code=None):
        url = ""
        if code is not None:
            url = "/" + code

        return self.client.get(
            "/otask/v1/tasks/companies/{0}/teams/{1}/tasks{2}".format(
                company, team, url
            )
        )
