# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2018 Upwork

# Updated by the script
"""Main package of the python bindings for Upwork API.

For convenience some most commonly used functionalities are imported here,
so you can use::

    from upwork import Client
    from upwork import raise_http_error

"""

VERSION = '1.3.4'


def get_version():
    return VERSION


from upwork.client import Client
from upwork.http import raise_http_error

__all__ = ["get_version", "Client", "raise_http_error"]
