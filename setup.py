#!/usr/bin/env python

from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-user-tracking',
    version='0.0.1',
    description='A user tracking package focusing on client side user tracking for Django.',
    author='Joe',
    author_email='joe@webv4.com',
    url='https://github.com/joebos/django-user-tracking',
    packages=find_packages(),
    package_data = {
        '': ['*.js', '*.py']
    },
    include_package_data=True,
    keywords = ["analytics", "tracking", "dashboard"],
    install_requires = [
        'django > 1.4',
        'django-rq',
        'rq'
    ],
    classifiers = [
        "Programming Language :: Python",
        "Programming Language :: JavaScript",
        "Development Status :: 2 - Alpha",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        ],
)
