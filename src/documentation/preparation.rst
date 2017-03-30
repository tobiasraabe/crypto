***********
Preparation
***********

Overview
========

While developing the project, it became clear that the whole data collection
process, especially Twitter, cannot be done after every
``python waf.py distclean``. Therefore, there are two implementations which
speed up the process and allow to start with previously generated data.

The first one is already mentioned in `installation`_ but we will cover it here
again. In the main folder of the project is a file called
``download_statics.py`` which will download a bunch of previously generated
Twitter data since 2014 from shared folder on Dropbox and extract the content
to ``src/static``. These files will be copied to ``bld/out/data_raw`` before
the processes in ``src/data_collection/wscript`` kick in.

How does ``src/data_collection/wscript`` work? Basically, the process takes the
information from ``src/data_collection/Poloniex/poloniex_config.yml`` and
starts to collect tweets for every key from the stated date on. Thereby, it
generates files where each file represents one week in a given year of tweets.
The files are called like this: ``twitter_<key>_<year>_<weeknumber>.csv``. The
process collects data until until it reaches the current date. The last and
incomplete datasets receive the suffix ``_partial.csv``.

Since we now know how data collection works, we can step back to
``preparation``. What was not mentioned is that the data collection process
does not only look at ``poloniex_config.yml`` but first looks in
``bld/out/data_raw`` for ``<key>.yml``. This file contains another date
which is the date until which we already have downloaded the Twitter data. This
date is preferred over the other so that we can specify a different date than
the original one to continue crawling the data.

Now, we have to do two things:

#. Check what is date of the latest crawled, complete chunk of week data
#. Enter that date in ``src/preparation/preparation.yml``


Adding new data
===============

If you want to add complete chunks of data to statics, you have to do two
things:

#. Copy the completed week file over to ``src/static``
#. Insert the last date in ``src/preparation/preparation.yml``


New Dropbox folder
==================

If you do not want to rely on the Dropbox of the current authors, feel free to
create your own download source. Just share a folder in the Dropbox and insert
the link in ``./download_statics.py`` under ``URL``. Make sure that the url
ends with ``?dl=1``. This ensures that all the content is downloaded as a zip
file.
