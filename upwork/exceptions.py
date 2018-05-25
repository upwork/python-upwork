# Python bindings to Upwork API
# python-upwork version 0.5
# (C) 2010-2015 Upwork

import logging
from upwork.compatibility import HTTPError


class BaseException(Exception):
    """Base exception class.

    Performs logging.

    """
    def __init__(self, *args, **kwargs):
        self.upwork_debug(*args, **kwargs)

    def upwork_debug(self, *args, **kwargs):
        logger = logging.getLogger('python-upwork')
        try:
            convert = unicode
        except NameError:
            convert = str
        logger.debug('{0}: {1}'.format(
            self.__class__.__name__,
            ', '.join(map(convert, args))))


class BaseHttpException(HTTPError, BaseException):

    def __init__(self, *args, **kwargs):
        self.upwork_debug(*args, **kwargs)
        super(BaseHttpException, self).__init__(*args, **kwargs)


class HTTP400BadRequestError(BaseHttpException):
    pass


class HTTP401UnauthorizedError(BaseHttpException):
    pass


class HTTP403ForbiddenError(BaseHttpException):
    pass


class HTTP404NotFoundError(BaseHttpException):
    pass


class InvalidConfiguredException(BaseException):
    pass


class APINotImplementedException(BaseException):
    pass


class AuthenticationError(BaseException):
    pass


class NotAuthenticatedError(BaseException):
    pass


class ApiValueError(BaseException):
    pass


class IncorrectJsonResponseError(BaseException):
    pass
