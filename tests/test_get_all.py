#!/usr/bin/env python

"""
Tests get_all()

@author john keck
@email robertjkeck2@gmail.com
"""

import unittest

from hackernews import HackerNews
from hackernews import Item


class TestGetAll(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_get_item(self):
        items = self.hn.get_all()
        self.assertIsInstance(items, list)
        self.assertIsInstance(items[0], Item)

    def tearDown(self):
    	self.hn.session.close()

if __name__ == '__main__':
    unittest.main()
