.. _data_collection:


***************
Data Collection
***************

This chapter of the documentation covers the process collecting data from various sources.


.. _poloniex_:

Poloniex
========

`Poloniex <https://poloniex.com/>`_  is a US-based cryptocurrency exchange and the project's trading place. Poloniex offers a pulbic API which can handles HTTP GET requests and answers via ``json`` data structures.


.. _twitter:

Twitter
=======

Short description of twitter and its value as an information source for our bot.

The way to retrieve data from Twitter was not to use its API. There are two reasons which make this way almost valueless.

1. There is a limit on API calls in a given time frame and its scope of data
2. The API only supports the last 7-9 days of data


.. _reddit:

Reddit
======

.. epigraph::

   Reddit is an American social news aggregation, web content rating, and discussion website. Reddit's registered community members can submit content, such as text posts or direct links. Registered users can then vote submissions up or down to organize the posts and determine their position on the site's pages. The submissions with the most positive votes appear on the front page or the top of a category. Content entries are organized by areas of interest called "subreddits". The subreddit topics include news, science, gaming, movies, music, books, fitness, food, and image-sharing, among many others. The site's terms of use prohibit behaviors such as harassment, and moderating and limiting harassment has taken substantial resources.

   -- `Wikipedia <https://en.wikipedia.org/wiki/Reddit>`_
