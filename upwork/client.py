# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

import os
import json
import logging
import urllib3

from urllib3 import Retry

from upwork.oauth import OAuth
from upwork.http import raise_http_error
from upwork.utils import decimal_default
from upwork.exceptions import IncorrectJsonResponseError

__all__ = ["Client"]

logger = logging.getLogger('python-upwork')

if os.environ.get("PYTHON_UPWORK_DEBUG", False):
    if os.environ.get("PYTHON_UPWORK_DEBUG_FILE", False):
        fh = logging.FileHandler(filename=os.environ["PYTHON_UPWORK_DEBUG_FILE"]
                                 )
        fh.setLevel(logging.DEBUG)
        logger.addHandler(fh)
    else:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        logger.addHandler(ch)
else:
    ch = logging.StreamHandler()
    ch.setLevel(logging.CRITICAL)
    logger.addHandler(ch)


class Client(object):
    """
    Main API client with oAuth v1 authorization.

    *Parameters:*
      :public_key:                Public API key

      :secret_key:                API key secret

      :oauth_access_token:        oAuth access token public key

      :oauth_access_token_secret: oAuth access token secret key

      :fmt:                       (optional, default ``json``)
                                  API response format.
                                  Currently only ``'json'`` is supported

      :finreport:                 (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.finreport` router

      :hr:                        (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.hr` router

      :messages:                  (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.messages` router

      :offers:                    (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.offers` router

      :provider:                  (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.provider` router

      :task:                      (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.task` router

      :team:                      (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.team` router

      :timereport:                (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.timereport` router

      :job:                       (optional, default ``True``)
                                  Whether to attach
                                  :py:mod:`upwork.routers.job` router

      :timeout:                   (optional, default ``8 secs``)
                                  Socket operations timeout.

      :poolmanager:               (optional, default ``None``)
                                  http connection pool manager
                                  from :py:mod:`urllib3.poolmanager`
    """

    def __init__(self, public_key, secret_key,
                 oauth_access_token=None, oauth_access_token_secret=None,
                 fmt='json', finreport=True, hr=True, messages=True,
                 offers=True, provider=True, task=True, team=True,
                 timereport=True, job=True, timeout=8, poolmanager=None):

        self.public_key = public_key
        self.secret_key = secret_key
        self.fmt = fmt

        # Catch the warning about
        # """
        # SecurityWarning: Certificate has no `subjectAltName`,
        # falling back to check for a `commonName` for now.
        # This feature is being removed by major browsers
        # and deprecated by RFC 2818.
        # (See https://github.com/shazow/urllib3/issues/497 for details.)
        # """
        # The warning will appear only in logs
        logging.captureWarnings(True)
        if poolmanager is None:
            from upwork import ca_certs_locater
            poolmanager = urllib3.PoolManager(
                cert_reqs='CERT_REQUIRED',
                ca_certs=ca_certs_locater.get(),
                timeout=urllib3.Timeout(connect=0.5, read=float(timeout)),
                retries=False
            )
        self.http = poolmanager

        self.oauth_access_token = oauth_access_token
        self.oauth_access_token_secret = oauth_access_token_secret

        # Namespaces
        self.auth = OAuth(self)

        if finreport:
            from upwork.routers.finreport import Finreports
            self.finreport = Finreports(self)

        if hr:
            from upwork.routers.hr import HR_V1, HR, HR_V3, HR_V4
            self.hr_v1 = HR_V1(self)
            self.hr = HR(self)
            self.hr_v3 = HR_V3(self)
            self.hr_v4 = HR_V4(self)

        if messages:
            from upwork.routers.messages import Messages
            self.messages = Messages(self)

        if offers:
            from upwork.routers.offers import Offers
            self.offers = Offers(self)

        if provider:
            from upwork.routers.provider import Provider, Provider_V2
            self.provider = Provider(self)
            self.provider_v2 = Provider_V2(self)

        if task:
            from upwork.routers.task import Task, Task_V2
            self.task = Task(self)
            self.task_v2 = Task_V2(self)

        if team:
            from upwork.routers.team import Team_V3
            self.team_v3 = Team_V3(self)

        if timereport:
            from upwork.routers.timereport import TimeReport
            self.timereport = TimeReport(self)

        if job:
            from upwork.routers.job import Job
            self.job = Job(self)

    # Shortcuts for HTTP methods
    def get(self, url, data=None):
        return self.read(url, data, method='GET', fmt=self.fmt)

    def post(self, url, data=None):
        return self.read(url, data, method='POST', fmt=self.fmt)

    def put(self, url, data=None):
        return self.read(url, data, method='PUT', fmt=self.fmt)

    def delete(self, url, data=None):
        return self.read(url, data, method='DELETE', fmt=self.fmt)

    # The method that actually makes HTTP requests
    def urlopen(self, url, data=None, method='GET', headers=None):
        """Perform oAuth v1 signed HTTP request.

        *Parameters:*
          :url:         Target url

          :data:        Dictionary with parameters

          :method:      (optional, default ``GET``)
                        HTTP method, possible values:
                          * ``GET``
                          * ``POST``
                          * ``PUT``
                          * ``DELETE``

          :headers:     (optional, default ``{}``)
                        Dictionary with header values

        """

        if headers is None:
            headers = {}

        self.last_method = method
        self.last_url = url
        self.last_data = data

        # TODO: Headers are not supported fully yet
        # instead we pass oauth parameters in querystring
        if method in ('PUT', 'DELETE'):
            post_data = self.auth.get_oauth_params(
                url, self.oauth_access_token,
                self.oauth_access_token_secret,
                {}, method)  # don't need parameters in url
        else:
            if data is None:
                data = {}
            post_data = self.auth.get_oauth_params(
                url, self.oauth_access_token,
                self.oauth_access_token_secret,
                data, method)

        if method == 'GET':
            url = '{0}?{1}'.format(url, post_data)
            return self.http.urlopen(method, url)
        elif method == 'POST':
            return self.http.urlopen(
                method, url, body=post_data,
                headers={'Content-Type':
                             'application/x-www-form-urlencoded;charset=UTF-8'})
        elif method in ('PUT', 'DELETE'):
            url = '{0}?{1}'.format(url, post_data)
            headers['Content-Type'] = 'application/json'
            if data is not None:
                data_json = json.dumps(data)
            else:
                data_json = ''
            return self.http.urlopen(
                method, url, body=data_json, headers=headers)

        else:
            raise Exception('Wrong http method: {0}. Supported'
                            'methods are: '
                            'GET, POST, PUT, DELETE'.format(method))

    def read(self, url, data=None, method='GET', fmt='json'):
        """
        Returns parsed Python object or raises an error.

        *Parameters:*
          :url:       Target url

          :data:      Dictionary with parameters

          :method:    (optional, default ``GET``)
                      HTTP method, possible values:
                        * ``GET``
                        * ``POST``
                        * ``PUT``
                        * ``DELETE``

          :fmt:         (optional, default ``json``)
                        API response format.
                        Currently only ``'json'`` is supported

        """
        assert fmt == 'json', "Only JSON format is supported at the moment"

        if '/gds/' not in url:
            url = '{0}.{1}'.format(url, fmt)

        logger = logging.getLogger('python-upwork')

        logger.debug('Prepairing to make Upwork call')
        logger.debug('URL: {0}'.format(url))
        try:
            logger.debug('Data: {0}'.format(
                json.dumps(data, default=decimal_default)))
        except TypeError:
            logger.debug('Data: {0}'.format(str(data)))
        logger.debug('Method: {0}'.format(method))
        response = self.urlopen(url, data, method)

        if response.status != 200:
            logger.debug('Error: {0}'.format(response))
            raise_http_error(url, response)

        result = response.data
        logger.debug('Response: {0}'.format(result))

        if fmt == 'json':
            try:
                result = json.loads(result)
            except ValueError:
                # Not a valid json string
                logger.debug('Response is not a valid json string')
                raise IncorrectJsonResponseError(
                    json.dumps({'status': response.status, 'body': result},
                               default=decimal_default)
                )
        return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()
