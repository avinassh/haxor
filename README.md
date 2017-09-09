# haxor

[![travis](https://img.shields.io/travis/avinassh/haxor.svg)](http://travis-ci.org/avinassh/haxor)
[![coverall](https://img.shields.io/coveralls/avinassh/haxor.svg)](https://coveralls.io/r/avinassh/haxor?branch=master)
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

import and initialization:
```python
from hackernews import HackerNews
hn = HackerNews()
```
Get certain user info by user id (i.e. username on Hacker News)
```python
user = hn.get_user('pg')
# >>> user.user_id
# pg
# >>> user.karma
# 155040
```
Stories, comments, jobs, Ask HNs and even polls are just items and they
have unique item id. To get info of an item by item id:
```python
item = hn.get_item(8863)
# >>> item.title
# "My YC app: Dropbox - Throw away your USB drive"
# >>> item.item_type
# story
# >>> item.kids
# [ 8952, 9224, 8917, ...]
```
To get item ids of current top stories:
```python
top_story_ids = hn.top_stories()
# >>> top_story_ids
# [8432709, 8432616, 8433237, ...]
```
To get current largest item id:
```python
max_item = hn.get_max_item()
# >>> max_item
# 8433746
```
Examples
========

Get top 10 stories:
```python
for story_id in hn.top_stories(limit=10):
    print hn.get_item(story_id)

# <hackernews.Item: 8432709 - Redis cluster, no longer vaporware>
# <hackernews.Item: 8432423 - Fluid Actuators from Disney Research Make Soft, Safe Robot Arms>
# <hackernews.Item: 8433237 - Is Capturing Carbon from the Air Practical?>
# ...
# ...
```
Find all the 'jobs' post from Top Stories:
```python
for story_id in hn.top_stories():
    story = hn.get_item(story_id)
    if story.item_type == 'job':
        print story

# <hackernews.Item: 8437631 - Lever (YC S12) hiring JavaScript experts, realtime systems engineers, to scale DerbyJS>
# <hackernews.Item: 8437036 - Product Designer (employee #1) to Organize the World's Code – Blockspring (YC S14)>
# <hackernews.Item: 8436584 - Django and iOS Hackers Needed – fix healthcare with Drchrono>
# ...
# ...
```
Find Python jobs from monthly who is hiring thread:
```python
# Who is hiring
# https://news.ycombinator.com/item?id=8394339

who_is_hiring = hn.get_item(8394339)

for comment_id in who_is_hiring.kids:
    comment = hn.get_item(comment_id)
    if 'python' in comment.text.lower():
        print comment.item_id

# 8395568
# 8394964
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
  

`get_user`
----------

Description: Returns `User` object

**Parameters:**

| Name         | Type     | Required   | Description                     | Default
| ------------ | -------- | ---------- | ------------------------------- | ---------
| `user_id`    | string   | Yes        | unique user id of a Hacker News user | None
                                                               

`top_stories`
-------------

Description: Returns list of item ids of current top stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`new_stories`
-------------

Description: Returns list of item ids of current new stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `limit`   | int   | No        | specifies the number of stories to be returned  | None
                                                            

`ask_stories`
-------------

Description: Returns list of item ids of latest Ask HN stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`show_stories`
-------------

Description: Returns list of item ids of latest Show HN stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`job_stories`
-------------

Description: Returns list of item ids of latest Job stories

**Parameters:**

| Name      | Type  | Required  | Description                           | Default
| --------- | ----- | --------- | ------------------------------------- | --------
| `limit`   | int   | No        | specifies the number of stories to be returned  | None


`updates`
--------------

Description: Returns list of item ids and user ids that have been changed/updated recently.


`get_max_item`
--------------

Description: Returns current largest item id

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
| kids        | The ids of the item’s comments, in ranked display order.
| url         | The URL of the story.
| score       | The story’s score, or the votes for a pollopt.
| title       | The title of the story or poll.
| parts       | A list of related pollopts, in display order.
| raw         | original JSON response.
| descendants | In the case of stories or polls, the total comment count.

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

Development
===========

For local development do `pip` installation of `requirements-dev.txt`:

    pip install -r requirements-dev.txt

LICENSE
=======

The mighty MIT license. Please check `LICENSE` for more details.
