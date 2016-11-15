# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

import logging
from six.moves.urllib.parse import urlparse, urlencode
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import HTTPError

from six.moves import http_client

from upwork.exceptions import HTTP400BadRequestError, HTTP401UnauthorizedError, \
    HTTP403ForbiddenError, HTTP404NotFoundError

UPWORK_ERROR_CODE = 'x-upwork-error-code'
UPWORK_ERROR_MESSAGE = 'x-upwork-error-message'

__all__ = ['raise_http_error']


def raise_http_error(url, response):
    """Raise custom ``urllib2.HTTPError`` exception.

    *Parameters:*
      :url:         Url that caused an error

      :response:    ``urllib3`` response object

    """
    status_code = response.status

    headers = response.getheaders()
    upwork_error_code = headers.get(UPWORK_ERROR_CODE, 'N/A')
    upwork_error_message = headers.get(UPWORK_ERROR_MESSAGE, 'N/A')

    formatted_msg = 'Code {0}: {1}'.format(upwork_error_code,
                                           upwork_error_message)

    if status_code == http_client.BAD_REQUEST:
        raise HTTP400BadRequestError(url, status_code, formatted_msg,
                                     headers, None)
    elif status_code == http_client.UNAUTHORIZED:
        raise HTTP401UnauthorizedError(url, status_code, formatted_msg,
                                       headers, None)
    elif status_code == http_client.FORBIDDEN:
        raise HTTP403ForbiddenError(url, status_code, formatted_msg,
                                    headers, None)
    elif status_code == http_client.NOT_FOUND:
        raise HTTP404NotFoundError(url, status_code, formatted_msg,
                                   headers, None)
    else:
        error = HTTPError(url, status_code, formatted_msg,
                          headers, None)
        logger = logging.getLogger('python-upwork')
        logger.debug(str(error))
        raise error
