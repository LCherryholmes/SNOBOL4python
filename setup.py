# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

VERSION = '0.3.4'
DESCRIPTION = 'Python SNOBOL4 package'
LONG_DESCRIPTION = 'SNOBOL4 string pattern matching for Python with regular expressions.'

setup(
    name='SNOBOL4python',
    version=VERSION,
    author="Lon Jones Cheryholmes",
    author_email="lcherryh@yahoo.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'SNOBOL', 'SNOBOL4', 'string pattern matching'],
    classifiers= []
)