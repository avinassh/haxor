#!/usr/bin/env python

"""
Tests top_stories()

@author avinash sajjanshetty
@email a@sajjanshetty.com
"""

import unittest

from hackernews import HackerNews


class TestTopStories(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_top_stories(self):
        top_stories = self.hn.top_stories()
        self.assertIsInstance(top_stories, list)
        self.assertIsNotNone(top_stories)


if __name__ == '__main__':
    unittest.main()
