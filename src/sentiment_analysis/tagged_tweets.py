#!/usr/bin/env python

"""This module performs a sentiment analysis of tweets by comparing downloaded
tweets with queries related to cryptocurrencies with the
*Stanford Twitter Corpus*.

An possible extension is the introduction of tagged tweets from the downloaded
dataset in the training set.

Due to the fact that the *Stanford Twitter corpus* is an arbitrary collection
of multiple topics, it is not adjusted to the topics of cryptocurrencies.
If a previous classifier, trained on the *Stanford Twitter Corpus*, is
extremely confident in its guess about a tweet from the
downloaded data, then it could be useful to include this tweet in a training
set to enhance performance on the topics of cryptocurrencies.

"""
