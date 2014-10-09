#!/usr/bin/env python

"""
haxor
Unofficial Python wrapper for official Hacker News API

@author avinash sajjanshetty
@email a@sajjanshetty.com
"""

import datetime
import json

import requests

class HackerNews(object):

    def __init__(self, version='v0'):
        self.base_url = 'https://hacker-news.firebaseio.com/{}/'.format(version)

    def _get(self, url):
        return requests.get(url)

    def _json2obj(self, json_data):
        pass

    def get_item(self, item_id):
        response = self._get('{0}item/{1}.json'.format(self.base_url, item_id))
        return Item(response.json())
        
    def get_user(self, user_id):
        response = self._get('{0}user/{1}.json'.format(self.base_url, user_id))
        return User(response.json())

    def top_stories(self, limit=None):
        response = self._get('{}topstories.json'.format(self.base_url))
        return response.json()[:limit]

    def get_max_item(self):
        response = self._get('{}maxitem.json'.format(self.base_url))
        return response.json()

class Item(object):
    """
    Represents stories, comments, jobs, Ask HNs and polls
    """

    def __init__(self, data):
        self.item_id = data.get('id')
        self.deleted = data.get('deleted')
        self.item_type = data.get('type')
        self.by = data.get('by')
        self.submission_time = datetime.datetime.fromtimestamp(data.get('time', 0))
        self.text = data.get('text')
        self.dead = data.get('dead')
        self.parent = data.get('parent')
        self.kids = data.get('kids')
        self.url = data.get('url')
        self.score = data.get('score')
        self.title = data.get('title')
        self.parts = data.get('parts')
        self.raw = json.dumps(data)

    def __repr__(self):
        return '{0}: {1}'.format(self.item_id, self.title)

class User(object):
    """
    Represents a hacker i.e. a user on Hacker News
    """

    def __init__(self, data):
        self.user_id = data.get('id')
        self.delay = data.get('delay')
        self.created = datetime.datetime.fromtimestamp(data.get('time', 0))
        self.karma = data.get('karma')
        self.about = data.get('about')
        self.submitted = data.get('submitted')
        self.raw = json.dumps(data)

    def __repr__(self):
        return '{0}: {1}'.format(self.user_id, self.karma)