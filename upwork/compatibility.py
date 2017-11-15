import sys


if sys.version_info > (3, 0, 0):
    from urllib import parse as urlparse
    from urllib.parse import quote, urlencode
    from urllib.error import HTTPError
    from http import client as httplib
else:
    import urlparse
    import httplib
    from urllib import quote, urlencode
    from urllib2 import HTTPError
