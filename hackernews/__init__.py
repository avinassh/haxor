#!/usr/bin/env python

"""
haxor
Unofficial Python wrapper for official Hacker News API

@author avinash sajjanshetty
@email hi@avi.im
"""

from __future__ import absolute_import
from __future__ import unicode_literals
import datetime
import json
import sys
from urllib.parse import urljoin

import requests
import aiohttp
import asyncio

from .settings import supported_api_versions

__all__ = [
    'User',
    'Item',
    'HackerNews',
    'InvalidAPIVersion',
    'InvalidItemID',
    'InvalidUserID']


class InvalidItemID(Exception):
    pass


class InvalidUserID(Exception):
    pass


class InvalidAPIVersion(Exception):
    pass


class HTTPError(Exception):
    pass


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.json()


async def fetch_all(session, urls, loop):
    tasks = [asyncio.ensure_future(fetch(session, url)) for url in urls]
    results = await asyncio.gather(*tasks)
    return results


class HackerNews(object):

    def __init__(self, version='v0'):
        """
        Args:
            version (string): specifies Hacker News API version.
            Default is `v0`.

        Raises:
          InvalidAPIVersion: If Hacker News version is not supported.

        """
        try:
            self.base_url = supported_api_versions[version]
        except KeyError:
            raise InvalidAPIVersion
        self.item_url = urljoin(self.base_url, 'item/')
        self.user_url = urljoin(self.base_url, 'user/')
        self.session = requests.Session()

    def _get_sync(self, url):
        response = self.session.get(url)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise HTTPError

    def _get_async(self, urls):
        """Internal method used for GET requests

        Args:
            urls (list): List of URLs to fetch.

        Returns:
            requests' response object

        Raises:
          HTTPError: If HTTP request failed.

        """
        loop = asyncio.get_event_loop()
        with aiohttp.ClientSession(loop=loop) as session:
            results = loop.run_until_complete(fetch_all(session, urls, loop))
        return results

    def get_user_by_ids(self, user_ids):
        """
        Given a list of user ids, return all the User objects
        """
        urls = [urljoin(self.user_url, F"{i}.json") for i in user_ids]
        result = self._get_async(urls=urls)
        return [User(r) for r in result]

    def get_story_by_ids(self, story_ids):
        """
        Given a list of story ids, return all the stories Item object
        """
        urls = [urljoin(self.item_url, F"{i}.json") for i in story_ids]
        result = self._get_async(urls=urls)
        return [Item(r) for r in result]

    def _get_stories(self, page, limit):
        """
        Hacker News has different categories (i.e. stories) like
        'topstories', 'newstories', 'askstories', 'showstories', 'jobstories'.
        This method, first fetches the relevant story ids of that category

        The URL is: https://hacker-news.firebaseio.com/v0/<story_name>.json

        e.g. https://hacker-news.firebaseio.com/v0/topstories.json

        Then, asynchronously it fetches each story and returns the Item objects

        The URL for individual story is:
            https://hacker-news.firebaseio.com/v0/item/<item_id>.json

        e.g. https://hacker-news.firebaseio.com/v0/item/69696969.json
        """
        url = urljoin(self.base_url, F"{page}.json")
        story_ids = self._get_sync(url)[:limit]
        return self.get_story_by_ids(story_ids=story_ids)

    def get_item(self, item_id):
        """Returns Hacker News `Item` object.

        Fetches the data from url:
            https://hacker-news.firebaseio.com/v0/item/<item_id>.json

        e.g. https://hacker-news.firebaseio.com/v0/item/69696969.json

        Args:
            item_id (int or string): Unique item id of Hacker News story,
            comment etc.

        Returns:
            `Item` object representing Hacker News item.

        Raises:
          InvalidItemID: If corresponding Hacker News story does not exist.

        """

        url = urljoin(self.item_url, F"{item_id}.json")
        response = self._get_sync(url)

        if not response:
            raise InvalidItemID

        return Item(response)

    def get_user(self, user_id):
        """Returns Hacker News `User` object.

        Fetches data from the url:
            https://hacker-news.firebaseio.com/v0/user/<user_id>.json

        e.g. https://hacker-news.firebaseio.com/v0/user/pg.json

        Args:
            user_id (string): unique user id of a Hacker News user.

        Returns:
            `User` object representing a user on Hacker News.

        Raises:
          InvalidUserID: If no such user exists on Hacker News.

        """
        url = urljoin(self.user_url, F"{user_id}.json")
        response = self._get_sync(url)

        if not response:
            raise InvalidUserID

        return User(response)

    def top_stories(self, limit=None):
        """Returns list of item ids of current top stories

        Args:
            limit (int): specifies the number of stories to be returned.

        Returns:
            `list` object containing ids of top stories.
        """
        return self._get_stories('topstories', limit)

    def new_stories(self, limit=None):
        """Returns list of item ids of current new stories

        Args:
            limit (int): specifies the number of stories to be returned.

        Returns:
            `list` object containing ids of new stories.
        """
        return self._get_stories('newstories', limit)

    def ask_stories(self, limit=None):
        """Returns list of item ids of latest Ask HN stories

        Args:
            limit (int): specifies the number of stories to be returned.

        Returns:
            `list` object containing ids of Ask HN stories.
        """
        return self._get_stories('askstories', limit)

    def show_stories(self, limit=None):
        """Returns list of item ids of latest Show HN stories

        Args:
            limit (int): specifies the number of stories to be returned.

        Returns:
            `list` object containing ids of Show HN stories.
        """
        return self._get_stories('showstories', limit)

    def job_stories(self, limit=None):
        """Returns list of item ids of latest Job stories

        Args:
            limit (int): specifies the number of stories to be returned.

        Returns:
            `list` object containing ids of Job stories.
        """
        return self._get_stories('jobstories', limit)

    def updates(self):
        """Returns list of item ids and user ids that have been
        changed/updated recently.

        Fetches data from URL:
            https://hacker-news.firebaseio.com/v0/updates.json

        Returns:
            `dict` with two keys whose values are `list` objects
        """
        url = urljoin(self.base_url, 'updates.json')
        response = self._get_sync(url)
        return {
            'items': self.get_story_by_ids(story_ids=response['items']),
            'profiles': self.get_user_by_ids(user_ids=response['profiles'])
        }

    def get_max_item(self):
        """The current largest item id

        Fetches data from URL:
            https://hacker-news.firebaseio.com/v0/maxitem.json

        Args:
            limit (int): specifies the number of stories to be returned.

        Returns:
            `int` if successful.
        """
        url = urljoin(self.base_url, 'maxitem.json')
        return self._get_sync(url)

    def get_all(self):
        """Returns ENTIRE Hacker News!

        Downloads all the HN articles and returns them as Item objects

        Returns:
            `list` object containing ids of HN stories.
        """
        max_item = self.get_max_item()
        return self.get_last(num=max_item)

    def get_last(self, num):
        """Returns last `num` of HN stories

        Downloads all the HN articles and returns them as Item objects

        Returns:
            `list` object containing ids of HN stories.
        """
        max_item = self.get_max_item()
        urls = [urljoin(self.item_url, F"{i}.json") for i in range(
            max_item - num + 1, max_item + 1)]
        result = self._get_async(urls=urls)
        return [Item(r) for r in result]


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
            data.get('time', 0))
        self.text = data.get('text')
        self.dead = data.get('dead')
        self.parent = data.get('parent')
        self.kids = data.get('kids')
        self.descendants = data.get('descendants')
        self.url = data.get('url')
        self.score = data.get('score')
        self.title = data.get('title')
        self.parts = data.get('parts')
        self.time = datetime.datetime.fromtimestamp(data.get('time'))
        self.raw = json.dumps(data)

    def __repr__(self):
        retval = '<hackernews.Item: {0} - {1}>'.format(
            self.item_id, self.title)
        if sys.version_info.major < 3:
            return retval.encode('utf-8', errors='backslashreplace')
        return retval


class User(object):

    """
    Represents a hacker i.e. a user on Hacker News
    """

    def __init__(self, data):
        self.user_id = data.get('id')
        self.delay = data.get('delay')
        self.created = datetime.datetime.fromtimestamp(data.get('created', 0))
        self.karma = data.get('karma')
        self.about = data.get('about')
        self.submitted = data.get('submitted')
        self.raw = json.dumps(data)

    def __repr__(self):
        retval = '<hackernews.User: {0}>'.format(self.user_id)
        if sys.version_info.major < 3:
            return retval.encode('utf-8', errors='backslashreplace')
        return retval
