# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.1'
DESCRIPTION = 'SNOBOL4 Python package'
LONG_DESCRIPTION = 'SNOBOL4 string pattern matching for Python.'

setup(
    name='SNOBOL4python',
    version=VERSION,
    author="Lon Jones Cheryholmes",
    author_email="lcherryh@yahoo.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'SNOBOL4', 'string pattern matching'],
    classifiers= []
)