# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork
from .compatibility import urlparse
from .config import BASE_URL

__all__ = ['Namespace', 'GdsNamespace']


class Namespace(object):
    """
    A special 'proxy' class to keep API methods organized.

    Use this class for defining new routers.

    """

    base_url = urlparse.urljoin(BASE_URL, 'api/')
    api_url = None
    version = 1

    def __init__(self, client):
        self.client = client

    def full_url(self, url):
        """
        Gets relative URL of API method and returns a full URL
        """
        return "{0}{1}v{2}/{3}".format(self.base_url,
                                       self.api_url, self.version, url)

    #Proxied client's methods
    def get(self, url, data=None):
        return self.client.get(self.full_url(url), data)

    def post(self, url, data=None):
        return self.client.post(self.full_url(url), data)

    def put(self, url, data=None):
        return self.client.put(self.full_url(url), data)

    def delete(self, url, data=None):
        return self.client.delete(self.full_url(url), data)


class GdsNamespace(Namespace):
    """Gds API only allows GET requests."""
    base_url = urlparse.urljoin(BASE_URL, 'gds/')

    def post(self, url, data=None):
        return None

    def put(self, url, data=None):
        return None

    def delete(self, url, data=None):
        return None
