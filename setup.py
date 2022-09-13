#!/usr/bin/env python

import sys
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='pickui',
    version="1.0",
    description='Advance file and folder picker for qpython',
    long_description="",
    author="guangrei",
    author_email='myawn@pm.me',
    py_modules=['pickui'],
    license='MIT',
    platforms='any',
)
