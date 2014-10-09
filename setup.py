try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.1.0'

setup(
    name='haxor',
    version=version,
    install_requires=['requests'],
    author='Avinash Sajjanshetty',
    author_email='a@sajjanshetty.com',
    packages=['hackernews', 'tests'],
    test_suite='tests',
    url='https://github.com/avinassh/haxor/',
    license='MIT License',
    description='Python wrapper for Hacker News API',
    long_description='Unofficial Python wrapper for official Hacker News API',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
    ],
)