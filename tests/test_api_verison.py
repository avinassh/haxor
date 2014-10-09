#!/usr/bin/env python

"""
Tests supported Hacker News API versions

@author avinash sajjanshetty
@email a@sajjanshetty.com
"""

import unittest

from hackernews import HackerNews
from hackernews import InvalidAPIVersion


class TestAPIVersion(unittest.TestCase):

    def test_valid_api_version_1(self):
        hn = HackerNews()
        self.assertIsInstance(hn, HackerNews)

    def test_valid_api_version_2(self):
        hn = HackerNews(version='v0')
        self.assertIsInstance(hn, HackerNews)

    def test_invalid_api_version(self):
        with self.assertRaises(InvalidAPIVersion):
            hn = HackerNews(version='v1')

if __name__ == '__main__':
    unittest.main()
