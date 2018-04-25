#!/usr/bin/env python

"""
Tests get_user()

@author avinash sajjanshetty
@email a@sajjanshetty.com
"""

import datetime
import unittest

from hackernews import HackerNews
from hackernews import Item, User


class TestGetUser(unittest.TestCase):

    def setUp(self):
        self.hn = HackerNews()

    def test_get_user(self):
        user = self.hn.get_user('pg')
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_id, 'pg')
        self.assertEqual(user.created,
                         datetime.datetime.fromtimestamp(1160418092))

    def test_get_user_expand(self):
        user = self.hn.get_user('avinassh', expand=True)
        self.assertIsInstance(user, User)
        self.assertEqual(user.user_id, 'avinassh')
        self.assertIsInstance(user.comments[0], Item)
        self.assertIsInstance(user.stories[0], Item)

    def tearDown(self):
    	self.hn.session.close()

if __name__ == '__main__':
    unittest.main()
