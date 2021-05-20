#!/usr/bin/env python

from setuptools import setup, find_packages  # type: ignore

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="Maksym Novozhylov",
    author_email="mnovozhilov@upwork.com",
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    description="Python bindings for Upwork API",
    install_requires=["requests_oauthlib>=1.3.0"],
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="python-upwork",
    name="python-upwork",
    packages=find_packages(),
    setup_requires=[],
    url="https://github.com/upwork/python-upwork",
    version="2.1.0",
    zip_safe=False,
)
