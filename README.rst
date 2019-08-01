.. image:: http://img.shields.io/packagist/l/upwork/php-upwork.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0.html
   :alt: License

.. image:: https://badge.fury.io/py/python-upwork.svg
   :target: http://badge.fury.io/py/python-upwork
   :alt: PyPI version

.. image:: https://img.shields.io/github/release/upwork/python-upwork.svg
   :target: https://github.com/upwork/python-upwork/releases
   :alt: GitHub release

.. image:: https://travis-ci.org/upwork/python-upwork.svg
   :target: http://travis-ci.org/upwork/python-upwork
   :alt: Build status

Copyright (c) 2010-2019, Upwork http://www.upwork.com
All rights reserved.


============================
Upwork API
============================
These are Python (**2, and 3 which is "supported" via unofficial PR #27 and not guaranteed**) bindings for Upwork Public API https://developers.upwork.com/
You can use the API to build apps that will help you:

* Manage your distributed team
* Search for contractors and jobs
* Send bulk invitations to interview and make offers
* Work with Messages workflow
* Retrieve Time & Financial information for your company, team and contractors

The API is the best way to communicate between apps.


Requirements
============
httplib2
oauth2
urllib3


Installation
============

    pip install python-upwork

All the dependencies will be automatically installed as well.


SSL Certificates Note
=====================
Package forces ``httplib2`` to use the OS's certificates file by default.

If you want to use your own certificates, introduce the following code during initialization::

    os.environ['HTTPLIB_CA_CERTS_PATH'] = '/path/to/my/ca_certs.txt'



Quick start
============
First, you need to create an API key for the authorization process here:
https://www.upwork.com/services/api/keys

Installing **Ipython** interactive shell is very useful for working
with the API. It offers features such as auto complete, history and docstring help display
if you add '?' to the end of the variable/function/class/method among other interesting functionalities.
So we really encourage you to install this shell: ``pip install ipython``

To get started, look at the docs http://upwork.github.io/python-upwork/how_to.html
and also look at the ``examples/`` folder to see examples how to
obtain oauth access tokens for web application and desktop application.


Useful Links
============

* `Git repo <http://github.com/upwork/python-upwork>`_
* `Issues <http://github.com/upwork/python-upwork/issues>`_
* `Documentation <http://upwork.github.io/python-upwork>`_
* `Mailing list <http://groups.google.com/group/python-upwork>`_
* `Facebook group <http://www.facebook.com/group.php?gid=136364403050710>`_
