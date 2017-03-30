.. _data_collection:


***************
Data Collection
***************

This chapter of the documentation covers the process collecting data from
various sources.


.. _poloniex_:

Poloniex
========

.. automodule:: src.data_collection.Poloniex.poloniex_data
    :members:


.. _twitter:

Twitter
=======

The idea that emotions affect our decision making is a key idea of behavioural
economics. Since decision on the micro-level are affected, the question is
whether emotions are also able to drive decisions in a way that even
macro-level variables are influenced.

Twitter is an obvious candidate to retrieve data from. The world-famous news
and social-networking service allows to share information up to 140 characters
long and has long been the target of researchers who want to study sentiments
(:ref:`pak2010`, :ref:`kouloumpis2011`, :ref:`go2009`).

Researchers

To collect data from Twitter, there are four possible options:

#. Twitter has an official API to retrieve its content, but there are two
   limits: first, Twitter restricts calls to the API by calls per day and the
   maximum amount of data per call. Second, one can only retrieve data for the
   last 7-9 days. These conditions render this approach useless since we need
   data for past market data.
#. `Gnip <https://gnip.com/sources/twitter/>`_ is the official data provider
   for Twitter but charges a lot of money. Again, not useful if we are just
   playing around.
#. We currently use `GetOldTweets-python`_ by Jefferson-Henrique which emulates
   a browser search on twitter on which no restrictions are posed. We included
   our fork of this package in our project since we adjusted it to our needs
   and implemented more options.
#. As a future source of Twitter data, we recently found a twitter stream
   on archive.org containing more than 4TB of data which you can find
   `here <https://archive.org/details/twitterstream>`_.

.. _GetOldTweets-python: https://github.com/Jefferson-Henrique/GetOldTweets-python

As previously described, we use `GetOldTweets-python`_ to collect data from
Twitter. Let us have a look at the main script:

.. code-block:: console

    $ python src/data_collection/Twitter/GetOldTweets-python/Exporter.py -h

    To use this script, you can pass the folowing attributes:
        username: Username of a specific twitter account (without @)
        since: The lower bound date (yyyy-mm-aa)
        until: The upper bound date (yyyy-mm-aa)
        querysearch: A query text to be matched
        maxtweets: The maximum number of tweets to retrieve
        filename: Enter a name for the file where the tweets are stored
        min_retweets: Enter the number of minimum retweets
        min_faves: Enter the number of minimum faves for tweets with youtube
                   vids


Future sources of information
=============================

.. _reddit:

Reddit
------

.. epigraph::

   Reddit is an American social news aggregation, web content rating, and
   discussion website. Reddit's registered community members can submit
   content, such as text posts or direct links. Registered users can then vote
   submissions up or down to organize the posts and determine their position on
   the site's pages. The submissions with the most positive votes appear on the
   front page or the top of a category. Content entries are organized by areas
   of interest called "subreddits". The subreddit topics include news, science,
   gaming, movies, music, books, fitness, food, and image-sharing, among many
   others. The site's terms of use prohibit behaviors such as harassment, and
   moderating and limiting harassment has taken substantial resources.

   -- `Wikipedia <https://en.wikipedia.org/wiki/Reddit>`_


`Bitcointalk <https://bitcointalk.org/>`_
-----------------------------------------

.. epigraph::

    Bitcoin Discussion General discussion about the Bitcoin ecosystem that
    doesn't fit better elsewhere.

    -- Bitcointalk website


.. bibliography:: ../paper/refs.bib

