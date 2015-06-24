#!/usr/bin/env python

"""
Tests updates()

@author avinash sajjanshetty
@email hi@avi.im
"""

import unittest

from hackernews import HackerNews


class TestUpdates(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_top_stories(self):
        updates = self.hn.updates()
        self.assertIsNotNone(updates)
        self.assertIsInstance(updates, dict)
        self.assertIsInstance(updates['profiles'], list)
        self.assertIsInstance(updates['items'], list)

if __name__ == '__main__':
    unittest.main()
