# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

import time
import oauth2 as oauth
import logging

from .compatibility import urlparse, urlencode
from .config import BASE_URL


from upwork.namespaces import Namespace


class OAuth(Namespace):

    """Authorization router.

    Has methods for retrieving access tokens and
    :py:meth:`~upwork.oauth.OAuth.get_info` method for
    checking you're authorized successfully and ready to work with API.
    """

    api_url = 'auth/'
    version = 1

    request_token_url = urlparse.urljoin(
        BASE_URL, 'api/auth/v1/oauth/token/request')
    authorize_url = urlparse.urljoin(BASE_URL, 'services/api/auth')
    access_token_url = urlparse.urljoin(BASE_URL, 'api/auth/v1/oauth/token/access')

    def get_oauth_params(self, url, key, secret, data=None, method='GET',
                         to_header=False, to_dict=False):
        """
        Converts a mapping object to signed url query.

        *Parameters:*
          :url:        Target url

          :key:        Public API key

          :secret:     Public API key secret

          :data:       Dictionary with data parameters

          :method:     Mehtod to be called, default is ``GET``

          :to_header:  If ``True``, data will be encoded as auth
                       headers

        """
        # Temporary not use incoming data, just generate headers
        if data is None:
            data = {}
        else:
            data = data.copy()

        token = oauth.Token(key, secret)
        consumer = self.get_oauth_consumer()
        data.update({
            'oauth_token': token.key,
            'oauth_consumer_key': consumer.key,
            'oauth_version': '1.0',
            'oauth_nonce': oauth.generate_nonce(),
            'oauth_timestamp': int(time.time()),
        })
        request = oauth.Request(method=method, url=url, parameters=data)
        signature_method = oauth.SignatureMethod_HMAC_SHA1()
        request.sign_request(signature_method, consumer, token)

        if to_header:
            return request.to_header()

        return request.to_postdata()

    def get_oauth_consumer(self):
        """
        Returns OAuth consumer object.
        """
        return oauth.Consumer(self.client.public_key, self.client.secret_key)

    def get_request_token(self):
        """
        Returns request token and request token secret.
        """
        client = oauth.Client(self.get_oauth_consumer())
        response, content = client.request(self.request_token_url, 'POST')
        if response.get('status') != '200':
            raise Exception(
                "Invalid request token response: {0}.".format(content))
        request_token = dict(urlparse.parse_qsl(content))
        self.request_token = request_token.get('oauth_token')
        self.request_token_secret = request_token.get('oauth_token_secret')
        return self.request_token, self.request_token_secret

    def get_authorize_url(self, callback_url=None):
        """
        Returns authentication URL to be used in a browser.
        """
        oauth_token = getattr(self, 'request_token', None) or\
            self.get_request_token()[0]
        if callback_url:
            params = urlencode({'oauth_token': oauth_token,\
                'oauth_callback': callback_url})
        else:
            params = urlencode({'oauth_token': oauth_token})
        return '{0}?{1}'.format(self.authorize_url, params)

    def get_access_token(self, verifier):
        """
        Returns access token and access token secret.
        """
        try:
            request_token = self.request_token
            request_token_secret = self.request_token_secret
        except AttributeError as e:
            logger = logging.getLogger('python-upwork')
            logger.debug(e)
            raise Exception("At first you need to call get_authorize_url")
        token = oauth.Token(request_token, request_token_secret)
        token.set_verifier(verifier)
        client = oauth.Client(self.get_oauth_consumer(), token)
        response, content = client.request(self.access_token_url, 'POST')
        if response.get('status') != '200':
            raise Exception(
                "Invalid access token response: {0}.".format(content))
        access_token = dict(urlparse.parse_qsl(content))
        self.access_token = access_token.get('oauth_token')
        self.access_token_secret = access_token.get('oauth_token_secret')
        return self.access_token, self.access_token_secret

    def get_info(self):
        """
        Get a detailed info about current authnticated user \
        and some data from his profile.

        """
        url = 'info'
        result = self.get(url)
        return result
