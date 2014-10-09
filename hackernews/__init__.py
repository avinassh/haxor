#!/usr/bin/env python

__all__ = [
    'User',
    'Item',
    'HackerNews',
    'InvalidAPIVersion',
    'InvalidItemID',
    'InvalidUserID']

"""
haxor
Unofficial Python wrapper for official Hacker News API

@author avinash sajjanshetty
@email a@sajjanshetty.com
"""

import datetime
import json

import requests

from settings import supported_api_versions


class InvalidItemID(Exception):
    pass


class InvalidUserID(Exception):
    pass


class InvalidAPIVersion(Exception):
    pass


class HackerNews(object):

    def __init__(self, version='v0'):
        try:
            self.base_url = supported_api_versions[version]
        except KeyError:
            raise InvalidAPIVersion

    def _get(self, url):
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return response
        else:
            raise Exception('HTTP Error: {}'.format(response.status_code))

    def get_item(self, item_id):
        response = self._get('{0}item/{1}.json'.format(self.base_url, item_id))

        if not response.json():
            raise InvalidItemID

        return Item(response.json())

    def get_user(self, user_id):
        response = self._get('{0}user/{1}.json'.format(self.base_url, user_id))

        if not response.json():
            raise InvalidUserID

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
        self.submission_time = datetime.datetime.fromtimestamp(
            data.get(
                'time',
                0))
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
