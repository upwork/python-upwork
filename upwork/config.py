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


class Config:
    """Configuration container"""

    verify_ssl = True

    def __init__(self, config):
        self.consumer_key, self.consumer_secret = (
            config["consumer_key"],
            config["consumer_secret"],
        )

        if "access_token" in config:
            self.access_token = config["access_token"]

        if "access_token_secret" in config:
            self.access_token_secret = config["access_token_secret"]

        if "verify_ssl" in config:
            self.verify_ssl = config["verify_ssl"]
