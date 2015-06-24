#!/usr/bin/env python

"""
Tests show_stories()

@author avinash sajjanshetty
@email hi@avi.im
"""

import unittest

from hackernews import HackerNews


class TestshowStories(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_show_stories(self):
        show_stories = self.hn.show_stories()
        self.assertIsInstance(show_stories, list)
        self.assertIsNotNone(show_stories)


if __name__ == '__main__':
    unittest.main()
