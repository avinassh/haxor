# haxor

![build](https://img.shields.io/github/actions/workflow/status/avinassh/haxor/pytest.yml)
[![coverall](https://coveralls.io/repos/github/avinassh/haxor/badge.svg?branch=master)](https://coveralls.io/github/avinassh/haxor?branch=master)
[![version](https://img.shields.io/pypi/v/haxor.svg)](https://pypi.python.org/pypi/haxor/)
[![supported](https://img.shields.io/pypi/pyversions/haxor.svg)](https://pypi.python.org/pypi/haxor/)
![license](https://img.shields.io/pypi/l/haxor.svg)

Unofficial Python wrapper for official Hacker News API.

Installation
============
```python
pip install haxor
```
Usage
=====

### Import and initialization:
```python
from hackernews import HackerNews
hn = HackerNews()
```

### Items
Stories, comments, jobs, Ask HNs and even polls are just items with unique item id.

To query item information by id:
```python
item = hn.get_item(8863)
# >>> item.title
# 'My YC app: Dropbox - Throw away your USB drive'
# >>> item.item_type
# 'story'
# >>> item.kids
# [ 8952, 9224, 8917, ...]
```
Since most results are returned as integer IDs (like item.kids above), these results require further iteration.  Instead of doing this yourself, use the `expand` flag to get object-oriented, detailed item info by id:
```python
item = hn.get_item(8863, expand=True)
# >>> item.kids
# [<hackernews.Item: 9224 - None>, <hackernews.Item: 8952 - None>, ...]
# >>> item.by
# <hackernews.User: dhouston>
```

To query a list of Item IDs:
```python
items = hn.get_items_by_ids([8863, 37236, 2345])
# >>> items
# [<hackernews.Item: 8863 - My YC app: Dropbox - Throw away your USB drive>, <hackernews.Item:
# 37236 - None>, <hackernews.Item: 2345 - The Best Buy Scam.>]
```
Use the `item_type` filter to specifically select 'story', 'comment', 'job', or 'poll' items:
```python
items = hn.get_items_by_ids([8863, 37236, 2345], item_type='story')
# >>> items
# [<hackernews.Item: 8863 - My YC app: Dropbox - Throw away your USB drive>, <hackernews.Item: # 2345 - The Best Buy Scam.>]
```

#### Stories
The HN API allows for real-time querying for New, Top, Best, Ask HN, Show HN, and Jobs stories.

As an example, to get Item objects of current top stories:
```python
top_stories = hn.top_stories()
# >>> top_stories
# [<hackernews.Item: 16924667 - Ethereum Sharding FAQ>, ...]
```

#### Useful Item Queries

To get current largest Item id (most recent story, comment, job, or poll):
```python
max_item = hn.get_max_item()
# >>> max_item
# 16925673
```
Once again, use the `expand` flag to get an object-oriented, detailed Item representation:
```python
max_item = hn.get_max_item(expand=True)
# >>> max_item
# <hackernews.Item: 16925673 - None>
```

To get the x most recent Items:
```python
last_ten = hn.get_last(10)
# >>> last_ten
# [<hackernews.Item: 16925688 - Show HN: Eventbot – Group calendar for Slack teams>, ...]
```

### Users
HN users are also queryable.

To query users by user_id (i.e. username on Hacker News):
```python
user = hn.get_user('pg')
# >>> user.user_id
# 'pg'
# >>> user.karma
# 155040
```
Use the `expand` flag to get an object-oriented, detailed Item representation for User attributes:
```python
user = hn.get_user('dhouston', expand=True)
# >>> user.stories
# [<hackernews.Item: 1481914 - Dropbox is hiring a Web Engineer>, ...]
# >>> user.comments
# [<hackernews.Item: 16660140 - None>, <hackernews.Item: 15692914 - None>, ...]
# >>> user.jobs
# [<hackernews.Item: 3955262 - Dropbox seeking iOS and Android engineers>, ...]
```

To query a list of users:
```python
users = hn.get_users_by_ids(['pg','dhouston'])
# >>> users
# [<hackernews.User: pg>, <hackernews.User: dhouston>]
```

Examples
========

Get top 10 stories:
```python
hn.top_stories(limit=10)

# [<hackernews.Item: 16924667 - Ethereum Sharding FAQ>, <hackernews.Item: 16925499 - PipelineDB # v0.9.9 – One More Release Until PipelineDB Is a PostgreSQL Extension>, ...]
```

Find all the 'jobs' post from Top Stories:
```python
stories = hn.top_stories()
for story in stories:
    if story.item_type == 'job':
        print(story)

# <hackernews.Item: 16925047 - Taplytics (YC W14) is solving hard engineering problems in
# Toronto and hiring>
# ...
# ...
```

Find Python jobs from monthly who is hiring thread:
```python
# Who is hiring - April 2018
# https://news.ycombinator.com/item?id=16735011

who_is_hiring = hn.get_item(16735011, expand=True)

for comment in who_is_hiring.kids:
    if 'python' in comment.text.lower():
        print(comment)

# <hackernews.Item: 16735358 - None>
# <hackernews.Item: 16737152 - None>
# ...
# ...
```

API Reference
=============

Class: `HackerNews`
===================

**Parameters:**

| Name       | Type   | Required  | Description                           | Default
| ---------- | ------ | --------- | ------------------------------------- | --------
| `version`  | string | No        | specifies Hacker News API version     | `v0`

`get_item`
----------

Description: Returns `Item` object

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `item_id`  | string/int| Yes      | unique item id of Hacker News story, comment etc | None
| `expand`   | bool      | No       | flag to indicate whether to transform all IDs into objects | False

`get_items_by_ids`
----------

Description: Returns list of `Item` objects

**Parameters:**


| Name       | Type      | Required | Description                         | Default
| ---------- | --------- | -------- | ----------------------------------- | -------
| `item_ids`  | list of string/int | Yes      | unique item ids of Hacker News stories, comments etc | None
| `item_type`   | string      | No       | item type to filter results with | None

`get_user`
----------

Description: Returns `User` object

**Parameters:**

| Name         | Type     | Required   | Description                     | Default
| ------------ | -------- | ---------- | ------------------------------- | ---------
| `user_id`    | string   | Yes        | unique user id of a Hacker News user | None
| `expand`   | bool      | No       | flag to indicate whether to transform all IDs into objects | False

`get_users_by_ids`
----------

Description: Returns list of `User` objects

**Parameters:**

| Name         | Type     | Required   | Description                     | Default
| ------------ | -------- | ---------- | ------------------------------- | ---------
| `user_ids`    | list of string/int  | Yes        | unique user ids of Hacker News users | None


`top_stories`
-------------

Description: Returns list of `Item` objects of current top stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `raw`   | bool   | No        | indicate whether to represent all objects in raw json  | False
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`new_stories`
-------------

Description: Returns list of `Item` objects of current new stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `raw`   | bool   | No        | indicate whether to represent all objects in raw json  | False
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`ask_stories`
-------------

Description: Returns list of `Item` objects of latest Ask HN stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `raw`   | bool   | No        | indicate whether to represent all objects in raw json  | False
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`show_stories`
-------------

Description: Returns list of `Item` objects of latest Show HN stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `raw`   | bool   | No        | indicate whether to represent all objects in raw json  | False
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`job_stories`
-------------

Description: Returns list of `Item` objects of latest Job stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `raw`   | bool   | No        | indicate whether to represent all objects in raw json  | False
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`updates`
--------------

Description: Returns list of `Item` and `User` objects that have been changed/updated recently.

**Parameters:**
N/A

`get_max_item`
--------------

Description: Returns current largest item id or current largest `Item` object

**Parameters:**

| Name         | Type     | Required   | Description                     | Default
| ------------ | -------- | ---------- | ------------------------------- | ---------
| `expand`   | bool      | No       | flag to indicate whether to transform ID into object | False

`get_all`
--------------

Description: Returns all `Item` objects from HN

**Parameters:**
N/A

`get_last`
--------------

Description: Returns list of `num` most recent `Item` objects

**Parameters:**

| Name         | Type     | Required   | Description                     | Default
| ------------ | -------- | ---------- | ------------------------------- | ---------
| `num`   | int      | No       | numbr of most recent records to pull from HN | 10

Class: `Item`
=============

From [Official HackerNews
Item](https://github.com/HackerNews/API/blob/master/README.md#items):

| Property    | Description
| ----------- | ------------------------------------------------------------
| item_id     | The item’s unique id.
| deleted     | `true` if the item is deleted.
| item_type   | The type of item. One of “job”, “story”, “comment”, “poll”, or “pollopt”.
| by          | The username of the item’s author.
| submission_time  | Creation date of the item, in Python `datetime`.
| text        | The comment, Ask HN, or poll text. HTML.
| dead        | `true` if the item is dead.
| parent      | The item’s parent. For comments, either another comment or the relevant story. For pollopts, the relevant poll.
| poll        | The ids of poll's.
| kids        | The ids of the item’s comments, in ranked display order.
| url         | The URL of the story.
| score       | The story’s score, or the votes for a pollopt.
| title       | The title of the story or poll.
| parts       | A list of related pollopts, in display order.
| descendants | In the case of stories or polls, the total comment count.
| raw         | original JSON response.


Class: `User`
=============

From [Official HackerNews
User](https://github.com/HackerNews/API/blob/master/README.md#users):

| Property  | Description
| --------- | -------------------------------------------------------------
| user_id   | The user’s unique username. Case-sensitive.
| delay     | Delay in minutes between a comment’s creation and its visibility to other users.
| created   | Creation date of the user, in Python `datetime`.
| karma     | The user’s karma.
| about     | The user’s optional self-description. HTML.
| submitted | List of the user’s stories, polls and comments.
| raw       | original JSON response.

Additional properties when `expand` is used

| Property    | Description
| ----------- | ------------------------------------------------------------
| stories  | The user’s submitted stories.
| comments     | The user's submitted comments.
| jobs   | The user's submitted jobs.
| polls   | The user's submitted polls.
| pollopts   | The user's submitted poll options.

Development
===========

For local development do `pip` installation of `requirements-dev.txt`:

    pip install -r requirements-dev.txt

Testing
=======

Run the test suite by running:

    echo "0.0.0-dev" > version.txt
    python setup.py develop
    pytest tests

LICENSE
=======

The mighty MIT license. Please check `LICENSE` for more details.
