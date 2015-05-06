.. image:: http://img.shields.io/packagist/l/upwork/php-upwork.svg
   :target: http://www.apache.org/licenses/LICENSE-2.0.html
   :alt: License

.. image:: https://badge.fury.io/py/python-upwork.svg
   :target: http://badge.fury.io/py/python-upwork
   :alt: PyPI version

.. image:: https://travis-ci.org/upwork/php-upwork.svg
   :target: http://travis-ci.org/upwork/php-upwork
   :alt: Build status

Copyright (c) 2010-2014, Upwork http://www.upwork.com
All rights reserved.


============================
Python bindings to Upwork API
============================

This is a Python bindings for Public Upwork API https://developers.upwork.com/
Using the API you can build apps that will help you:

* Mangage your distributed team
* Search for contractors and jobs
* Send bulk invitations to interview and make offers
* Send bulk messages to your team
* Retrieve Time & Financial information for your company, team and contractors

API is the best way to comunicate between apps.


Requirements
============
httplib2==0.9
oauth2==1.5.211
urllib3==1.10
httplib2.system-ca-certs-locater==0.1.1

Installation
============

    pip install python-upwork

All the dependencies will be automatically installed as well.


SSL Certificates Note
=====================
We recomend to install a package ``httplib2.system_ca_certs_locater`` (it is installed by default during ``python_upwork`` installation)::

    pip install pbr httplib2.system_ca_certs_locater

It will force ``httplib2`` to use the OS's certificates file.

If you want to use your own certificates, put the following code during initialization::

    os.environ['HTTPLIB_CA_CERTS_PATH'] = '/path/to/my/ca_certs.txt'



Quickstart
==========
First, you need to create API key for authorization here:
https://www.upwork.com/services/api/keys

Installing **Ipython** interactive shell is very useful for playing
with the API, it has autocomplete, history, displays docstring help if you add '?'
to the end of variable/function/class/method and many other nice things.
So we greatly encourage you to install it: ``pip install ipython``

To get started, look at the docs http://upwork.github.io/python-upwork/how_to.html
and also look at the ``examples/`` folder to see examples how to
obtain oauth access tokens for web application and desktop application.

Also threre's a list of opensource projects using ``python-upwork``:

* Upwork Meter https://github.com/kipanshi/upwork_meter
* Upwork Graphs https://github.com/demalexx/upwork-graphs


Useful Links
============

* `Git repo <http://github.com/upwork/python-upwork>`_
* `Issues <http://github.com/upwork/python-upwork/issues>`_
* `Documentation <http://upwork.github.com/python-upwork/>`_
* `Mailing list <http://groups.google.com/group/python-upwork>`_
* `Facebook group <http://www.facebook.com/group.php?gid=136364403050710>`_
