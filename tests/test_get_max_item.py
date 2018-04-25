#!/usr/bin/env python

"""
Tests get_max_item()

@author avinash sajjanshetty
@email a@sajjanshetty.com
"""

import unittest

from hackernews import HackerNews


class TestGetMaxItem(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_get_max_item(self):
        max_item_id = self.hn.get_max_item()
        self.assertIsInstance(max_item_id, int)

    def tearDown(self):
    	self.hn.session.close()

if __name__ == '__main__':
    unittest.main()
