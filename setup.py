#!/usr/bin/env python

from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md', encoding='utf-8').read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open('version.txt') as f:
    version = f.read().strip()

setup(
    name='haxor',
    version=version,
    install_requires=requirements,
    author='Avinash Sajjanshetty',
    author_email='a@sajjanshetty.com',
    packages=find_packages(),
    include_package_data=True,
    test_suite='tests',
    url='https://github.com/avinassh/haxor/',
    license='MIT',
    description='Unofficial Python wrapper for Hacker News API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)
