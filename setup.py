#!/usr/bin/env python

import os
import sys

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__author__ = 'Alec Cunningham <aleccunningham96@gmail.com>'
__version__ = '0.1'

packages = [
    'pygci',
]

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name='pygci',
    version=__version__,
    install_requires=['requests>=2.1.0'],
    author='Alec Cunningham',
    author_email='aleccunningham96@gmail.com',
    license=open('LICENSE').read(),
    url='https://github.com/aleccunningham/pygci/tree/master',
    keywords='Google Civic Information api',
    description='Simple Python wrapper for the Google Civic Information API',
    include_package_data=True,
    packages=packages,
)
