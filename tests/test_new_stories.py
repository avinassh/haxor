#!/usr/bin/env python

"""
Tests new_stories()

@author avinash sajjanshetty
@email hi@avi.im
"""

import unittest

from hackernews import HackerNews


class TestNewStories(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_new_stories(self):
        new_stories = self.hn.new_stories()
        self.assertIsInstance(new_stories, list)
        self.assertIsNotNone(new_stories)


if __name__ == '__main__':
    unittest.main()
