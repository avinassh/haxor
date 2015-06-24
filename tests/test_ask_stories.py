#!/usr/bin/env python

"""
Tests ask_stories()

@author avinash sajjanshetty
@email hi@avi.im
"""

import unittest

from hackernews import HackerNews


class TestaskStories(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_ask_stories(self):
        ask_stories = self.hn.ask_stories()
        self.assertIsInstance(ask_stories, list)
        self.assertIsNotNone(ask_stories)


if __name__ == '__main__':
    unittest.main()
