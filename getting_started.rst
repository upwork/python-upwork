.. _getting_started:


***************
Getting started
***************

..
.. _requirements:

Requirements
-----------------
You need to install oauth2 and urllib3 to run the python-upwork. These packages are installed automatically, so basicly you don't need to install them manually.

If you want to contribute to python-upwork, you need to istall ``mock`` and ``nosetests``.

Mock::

    pip install mock
    #or
    easy_install mock

Nosetests::

    pip install nose
    #or
    easy_install nose

.. _install:

Install
-----------------
On most UNIX-like systems, you’ll probably need to run these commands as root or using sudo.

To install via pip::

    pip install python-upwork

Or via easy_install::

    easy_install python-upwork

Or install from source::

    python setup.py install

Also, you can retrieve the most recent version of python-upwork from GitHub::

    git clone git://github.com/upwork/python-upwork.git

.. _settings:

Settings
---------------------

You will need to use your public and private Upwork API keys::

    client = upwork.Client('your public key', 'your secret key')

To get Upwork API keys, please visit the http://www.upwork.com/services/api/keys

.. _simple_example:

Simple Example
---------------------
This example is very easy to follow in Python interactive console,
we also recommend to use improved interactive console - IPython.

You can see the full code of examples in ``examples`` folder.

Here is the simple example if you are using web API keys.

Initializing the client::

    client = upwork.Client(public_key, secret_key)

Now follow the ``authorize_url``::

    print client.auth.get_authorize_url()

After you follow this url you'll be redirected to the callback url that you
entered during API keys creation. The ``oauth_verifier`` parameter is passed to the callback
and you need to copy it's value. If you selected "Desktop" type of the key instead
of "Web", the value of oAuth verifier will be just displayed to you.

Now you get the verifier copied into your buffer and you can get you access token::

    verifier = raw_input('Enter oauth_verifier: ')
    oauth_access_token, oauth_access_token_secret = client.auth.get_access_token(verifier)

Great! Now you got all the necessary credentials for accessing the Upwork API.
Use obtained ``oauth_access_token`` and ``oauth_access_token_secret`` to intialize
a ready-to-go Client instance::

    client = upwork.Client(public_key, secret_key,
                          oauth_access_token=oauth_access_token,
                          oauth_access_token_secret=oauth_access_token_secret)

To check it works::

    print client.auth.get_info()

This call will give you information about the currently authorized user.

.. note:: Make sure you securely store the ``oauth_access_token`` and ``oauth_access_token_secret``.


So now just start playing with the API, for example you can get your teamrooms::

    print client.team.get_teamrooms()

or get your companies::

    print client.hr.get_companies()


See the Reference Documentation for the full list of available API calls
:ref:`reference_docs`
