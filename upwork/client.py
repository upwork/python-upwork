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

import requests
from . import upwork
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests_oauthlib import OAuth1 # type: ignore
from urllib.parse import parse_qsl, urlencode


class Client(object):
    """API client for OAuth1 authorization
    
    *Parameters:*
    :config: An instance of upwork.Config class, which contains the configuration keys and tokens
    """

    __data_format = "json"
    __overload_var = "http_method"

    __uri_auth = "/services/api/auth"
    __uri_rtoken = "/auth/v1/oauth/token/request"
    __uri_atoken = "/auth/v1/oauth/token/access"

    epoint = upwork.DEFAULT_EPOINT

    def __init__(self, config):
        self.config = config

        self.requests = requests.Session()
        self.requests.mount('https://', HTTPAdapter(max_retries=Retry(total=0)))

    def get_request_token(self):
        """Get request token"""
        oauth = OAuth1(self.config.consumer_key, self.config.consumer_secret)
        request_token_url = full_url(self.__uri_rtoken, upwork.DEFAULT_EPOINT)

        try:
            r = requests.post(url=request_token_url, auth=oauth, verify=self.config.verify_ssl)
        except Exception as e:
            raise e

        rtoken_response = dict(parse_qsl(r.content.decode("utf8")))
        self.request_token = rtoken_response.get("oauth_token")
        self.request_token_secret = rtoken_response.get("oauth_token_secret")

        return self.request_token, self.request_token_secret

    def get_authorization_url(self, callback_url=None):
        """Get authorization URL

        :param callback_url:  (Default value = None)

        """
        oauth_token = (
            getattr(self, "request_token", None) or self.get_request_token()[0]
        )

        if callback_url:
            params = urlencode(
                {"oauth_token": oauth_token, "oauth_callback": callback_url}
            )
        else:
            params = urlencode({"oauth_token": oauth_token})

        return "{0}{1}?{2}".format(upwork.BASE_HOST, self.__uri_auth, params)

    def get_access_token(self, verifier):
        """Returns access token and access token secret

        :param verifier: 

        """
        try:
            request_token = self.request_token
            request_token_secret = self.request_token_secret
        except AttributeError as e:
            raise Exception(
                "Request token pair not found. You need to call get_authorization_url"
            )

        oauth = OAuth1(
            self.config.consumer_key,
            client_secret=self.config.consumer_secret,
            resource_owner_key=self.request_token,
            resource_owner_secret=self.request_token_secret,
            verifier=verifier,
        )

        access_token_url = full_url(self.__uri_atoken, upwork.DEFAULT_EPOINT)

        try:
            r = requests.post(url=access_token_url, auth=oauth, verify=self.config.verify_ssl)
        except Exception as e:
            raise e

        atoken_response = dict(parse_qsl(r.content.decode("utf8")))
        self.config.access_token = atoken_response.get("oauth_token")
        self.config.access_token_secret = atoken_response.get("oauth_token_secret")

        return self.config.access_token, self.config.access_token_secret

    def get(self, uri, params=None):
        """Execute GET request

        :param uri: 
        :param params:  (Default value = None)

        """
        return self.send_request(uri, "get", params)

    def post(self, uri, params=None):
        """Execute POST request

        :param uri: 
        :param params:  (Default value = None)

        """
        return self.send_request(uri, "post", params)

    def put(self, uri, params=None):
        """Execute PUT request

        :param uri: 
        :param params:  (Default value = None)

        """
        return self.send_request(uri, "put", params)

    def delete(self, uri, params=None):
        """Execute DELETE request

        :param uri: 
        :param params:  (Default value = None)

        """
        return self.send_request(uri, "delete", params)

    def send_request(self, uri, method="get", params={}):
        """Send request

        :param uri: 
        :param method:  (Default value = 'get')
        :param params:  (Default value = {})

        """
        # delete does not support passing the parameters
        if method == "delete":
            params[self.__overload_var] = method

        oauth = OAuth1(
            self.config.consumer_key,
            client_secret=self.config.consumer_secret,
            resource_owner_key=self.config.access_token,
            resource_owner_secret=self.config.access_token_secret,
            signature_type="query",
        )

        url = full_url(get_uri_with_format(uri, self.epoint), self.epoint)

        if method == "get":
            r = self.requests.get(url, params=params, auth=oauth, verify=self.config.verify_ssl)
        elif method == "put":
            headers = {"Content-type": "application/json"}
            r = self.requests.put(url, json=params, headers=headers, auth=oauth, verify=self.config.verify_ssl)
        elif method in {"post", "delete"}:
            headers = {"Content-type": "application/json"}
            r = self.requests.post(url, json=params, headers=headers, auth=oauth, verify=self.config.verify_ssl)
        else:
            raise ValueError(
                'Do not know how to handle http method "{0}"'.format(method)
            )

        return r.json()


"""

"""


def full_url(uri, epoint=None):
    """Get full URL

    :param uri: 
    :param epoint:  (Default value = None)

    """
    if not epoint:
        epoint = upwork.DEFAULT_EPOINT
    return "{0}/{1}{2}".format(upwork.BASE_HOST, epoint, uri)


def get_uri_with_format(uri, epoint):
    """Get URI with format ending

    :param uri: 
    :param epoint: 

    """
    if epoint == upwork.DEFAULT_EPOINT:
        uri += ".json"
    return uri
