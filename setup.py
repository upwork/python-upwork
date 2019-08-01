# Copyright (c) 2010-2014, Upwork http://www.upwork.com
# All rights reserved.
from __future__ import print_function

import re
import os
from setuptools import setup, find_packages
from distutils.core import Command

readme = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
README = readme.read()
readme.close()

VERSION = (1, 3, 4, 0, 0)


def get_version():
    version = '{0}.{1}'.format(VERSION[0], VERSION[1])
    if VERSION[2]:
        version = '{0}.{1}'.format(version, VERSION[2])
    if VERSION[3:] == ('alpha', 0):
        version = '{0} pre-alpha'.format(version)
    else:
        if VERSION[3] != 0:
            version = "{0}.{1}".format(version, VERSION[3])
            if VERSION[4] != 0:
                version = '{0} {1}'.format(version, VERSION[4])
    return version


def update_init(version):
    """Update version number in the ``upwork/__init__.py``.

    """
    print('Updating ``upwork/__init__.py`` to version "{0}"'.format(version))
    # Update 'VERSION' variable in ``upwork/__init__.py``
    with open('upwork/__init__.py', 'r') as f:
        init_contents = f.read()

    new_init = re.sub(
        '(VERSION = \'[a-zA-Z0-9\.\s]*\')',
        'VERSION = \'{0}\''.format(version), init_contents)

    # Write backup
    with open('upwork/__init__.py.back', 'w') as f:
        f.write(init_contents)

    # Write new init
    with open('upwork/__init__.py', 'w') as f:
        f.write(new_init)

    print('OK')


class UpdateVersion(Command):

    description = 'update version in ``upwork/__init__.py``'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        update_init(get_version())


setup(cmdclass={'update_version': UpdateVersion},
      name='python-upwork',
      version=get_version(),
      description='Python bindings to Upwork API',
      long_description=README,
      author='Upwork',
      author_email='python@upwork.com',
      maintainer='Maksym Novozhylov',
      maintainer_email='mnovozhilov@upwork.com',
      install_requires=['oauth2==1.9.0.post1', 'urllib3==1.25.3'],
      packages=find_packages(),
      license='BSD',
      download_url='http://github.com/upwork/python-upwork',
      url='http://upwork.github.com/python-upwork',
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Environment :: Web Environment',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Software Development '
                       ':: Libraries :: Python Modules',
                   'Topic :: Utilities'])
