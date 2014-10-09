#!/usr/bin/env python

from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='haxor',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/avinassh/haxor/',
    license='MIT',
    author='Avinash Sajjanshetty',
    author_email='a@sajjanshetty.com',
    description='Unofficial Python wrapper for official Hacker News API',
    install_requires=requirements
)