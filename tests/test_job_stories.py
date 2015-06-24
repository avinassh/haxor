#!/usr/bin/env python

"""
Tests job_stories()

@author avinash sajjanshetty
@email hi@avi.im
"""

import unittest

from hackernews import HackerNews


class TestjobStories(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_job_stories(self):
        job_stories = self.hn.job_stories()
        self.assertIsInstance(job_stories, list)
        self.assertIsNotNone(job_stories)


if __name__ == '__main__':
    unittest.main()
