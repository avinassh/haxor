#!/usr/bin/env python

"""
Tests supported Hacker News API versions

@author john keck
@email robertjkeck2@gmail.com
"""

import unittest

from test_api_version import TestAPIVersion
from test_ask_stories import TestAskStories
from test_get_item import TestGetItem 
from test_get_items_by_ids import TestGetItemsByIDs 
from test_get_last import TestGetLast 
from test_get_max_item import TestGetMaxItem 
from test_get_user import TestGetUser 
from test_get_users_by_ids import TestGetUsersByIDs 
from test_job_stories import TestJobStories
from test_new_stories import TestNewStories 
from test_show_stories import TestShowStories 
from test_top_stories import TestTopStories 
from test_updates import TestUpdates

if __name__ == '__main__':
	unittest.main()
