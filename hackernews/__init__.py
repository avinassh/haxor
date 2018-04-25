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
        """Internal method used for GET requests
        
        Args:
            url (str): URL to fetch
        
        Returns:
            Individual URL request's response
        
        Raises:
          HTTPError: If HTTP request failed.
        """
        response = self.session.get(url)
        if response.status_code == requests.codes.ok:
            return response.json()
        else:
            raise HTTPError

    async def _get_async(self, url, session):
        """Asynchronous internal method used for GET requests
        
        Args:
            url (str): URL to fetch
            session (obj): aiohttp client session for async loop
        
        Returns:
            data (obj): Individual URL request's response corountine
        
        """
        try:
            async with session.get(url) as resp:
                data = await resp.json()
        except:
            data = None
        return data

    async def _async_loop(self, urls):
        """Asynchronous internal method used to request multiple URLs
        
        Args:
            urls (list): URLs to fetch
        
        Returns:
            responses (obj): All URL requests' response coroutines
        
        """
        results = []
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            for url in urls:
                result = asyncio.ensure_future(self._get_async(url, session))
                results.append(result)
            responses = await asyncio.gather(*results)
        return responses

    def _run_async(self, urls):
        """Asynchronous event loop execution
        
        Args:
            urls (list): URLs to fetch
        
        Returns:
            results (obj): All URL requests' responses
        
        """
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(self._async_loop(urls))
        return results

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
        return self.get_items_by_ids(item_ids=story_ids)

    def get_item(self, item_id, expand=False):
        """Returns Hacker News `Item` object.
        
        Fetches the data from url:
            https://hacker-news.firebaseio.com/v0/item/<item_id>.json
        
        e.g. https://hacker-news.firebaseio.com/v0/item/69696969.json
        
        Args:
            item_id (int or string): Unique item id of Hacker News story,
            comment etc.
            expand (bool): expand (bool): Flag to indicate whether to transform all IDs into objects.
        
        Returns:
            `Item` object representing Hacker News item.
        
        Raises:
          InvalidItemID: If corresponding Hacker News story does not exist.
        
        """
        url = urljoin(self.item_url, F"{item_id}.json")
        response = self._get_sync(url)

        if not response:
            raise InvalidItemID
        else:
            item = Item(response)
            if expand:
                item.by = self.get_user(item.by)
                item.kids = self.get_items_by_ids(item.kids) if item.kids else None
                item.parent = self.get_item(item.parent) if item.parent else None
                item.poll = self.get_item(item.poll) if item.poll else None
                item.parts = self.get_items_by_ids(item.parts) if item.parts else None

        return item

    def get_items_by_ids(self, item_ids, item_type=None):
        """Given a list of item ids, return all the Item objects

        Args:
            item_ids (obj): List of item IDs to query
            item_type (str): (optional) Item type to filter results with

        Returns:
            List of `Item` objects for given item IDs and given item type

        """
        urls = [urljoin(self.item_url, F"{i}.json") for i in item_ids]
        result = self._run_async(urls=urls)
        items = [Item(r) for r in result if r]
        if item_type:
            return [item for item in items if item.item_type == item_type]
        else:
            return items

    def get_user(self, user_id, expand=False):
        """Returns Hacker News `User` object.
        
        Fetches data from the url:
            https://hacker-news.firebaseio.com/v0/user/<user_id>.json
        
        e.g. https://hacker-news.firebaseio.com/v0/user/pg.json
        
        Args:
            user_id (string): unique user id of a Hacker News user.
            expand (bool): Flag to indicate whether to transform all IDs into objects.
        
        Returns:
            `User` object representing a user on Hacker News.
        
        Raises:
          InvalidUserID: If no such user exists on Hacker News.
        
        """
        url = urljoin(self.user_url, F"{user_id}.json")
        response = self._get_sync(url)

        if not response:
            raise InvalidUserID
        else:
            user = User(response)
            if expand and user.submitted:
                submitted_items = self.get_items_by_ids(user.submitted)
                user.stories = [item for item in submitted_items if item.item_type == 'story']
                user.comments = [item for item in submitted_items if item.item_type == 'comment']
                user.jobs = [item for item in submitted_items if item.item_type == 'job']
                user.polls = [item for item in submitted_items if item.item_type == 'poll']
                user.pollopts = [item for item in submitted_items if item.item_type == 'pollopt']

        return user

    def get_users_by_ids(self, user_ids):
        """
        Given a list of user ids, return all the User objects
        """
        urls = [urljoin(self.user_url, F"{i}.json") for i in user_ids]
        result = self._run_async(urls=urls)
        return [User(r) for r in result if r]

    def top_stories(self, raw=False, limit=None):
        """Returns list of item ids of current top stories
        
        Args:
            limit (int): specifies the number of stories to be returned.
            raw (bool): Flag to indicate whether to transform all objects into raw json.
        
        Returns:
            `list` object containing ids of top stories.
        
        """
        if raw:
            return [story.raw for story in self._get_stories('topstories', limit)]
        else:
            return self._get_stories('topstories', limit)

    def new_stories(self, raw=False, limit=None):
        """Returns list of item ids of current new stories
        
        Args:
            limit (int): specifies the number of stories to be returned.
            raw (bool): Flag to indicate whether to transform all objects into raw json.
        
        Returns:
            `list` object containing ids of new stories.
        
        """
        if raw:
            return [story.raw for story in self._get_stories('newstories', limit)]
        else:
            return self._get_stories('newstories', limit)

    def ask_stories(self, raw=False, limit=None):
        """Returns list of item ids of latest Ask HN stories
        
        Args:
            limit (int): specifies the number of stories to be returned.
            raw (bool): Flag to indicate whether to transform all objects into raw json.
        
        Returns:
            `list` object containing ids of Ask HN stories.
        
        """
        if raw:
            return [story.raw for story in self._get_stories('askstories', limit)]
        else:
            return self._get_stories('askstories', limit)

    def show_stories(self, raw=False, limit=None):
        """Returns list of item ids of latest Show HN stories
        
        Args:
            limit (int): specifies the number of stories to be returned.
            raw (bool): Flag to indicate whether to transform all objects into raw json.
        
        Returns:
            `list` object containing ids of Show HN stories.
        
        """
        if raw:
            return [story.raw for story in self._get_stories('showstories', limit)]
        else:
            return self._get_stories('showstories', limit)

    def job_stories(self, raw=False, limit=None):
        """Returns list of item ids of latest Job stories
        
        Args:
            limit (int): specifies the number of stories to be returned.
            raw (bool): Flag to indicate whether to transform all objects into raw json.
        
        Returns:
            `list` object containing ids of Job stories.
        
        """
        if raw:
            return [story.raw for story in self._get_stories('jobstories', limit)]
        else:
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
            'items': self.get_items_by_ids(item_ids=response['items']),
            'profiles': self.get_users_by_ids(user_ids=response['profiles'])
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
        result = self._run_async(urls=urls)
        return [Item(r) for r in result if r]


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
        self.poll = data.get('poll')
        self.kids = data.get('kids')
        self.url = data.get('url')
        self.score = data.get('score')
        self.title = data.get('title')
        self.parts = data.get('parts')
        self.descendants = data.get('descendants')
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
