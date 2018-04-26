#!/usr/bin/env python

"""
Tests get_all()

@author john keck
@email robertjkeck2@gmail.com
"""

import unittest

from hackernews import HackerNews
from hackernews import Item


class TestAll(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    @unittest.skip("Skip for timeout issue due to long runtime")
    def test_get_all(self):
        items = self.hn.get_all()
        self.assertIsInstance(items, list)
        self.assertIsInstance(items[0], Item)

    def tearDown(self):
        self.hn.session.close()

if __name__ == '__main__':
    unittest.main()
