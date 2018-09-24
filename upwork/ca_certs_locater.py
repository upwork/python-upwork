import os

LINUX_PATH = '/etc/ssl/certs/ca-certificates.crt'

# openssl installed using `brew install openssl`
OSX_PATH = '/usr/local/etc/openssl/cert.pem'


def get():
    """Return a path to a certificate authority file.
    """
    # FIXME(dhellmann): Assume Linux for now, add more OSes and
    # platforms later.

    if os.path.exists(LINUX_PATH):
        return LINUX_PATH

    if os.path.exists(OSX_PATH):
        return OSX_PATH

    # Fall back to the httplib2 default behavior by raising an
    # ImportError if we have not found the file.
    raise ImportError()
