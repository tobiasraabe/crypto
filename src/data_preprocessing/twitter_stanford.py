#!/usr/bin/env python

import datetime
import pandas as pd

from dateutil import parser
from sklearn.externals import joblib
from bld.project_paths import project_paths_join as ppj


def dateparse(date):
    return parser.parse(date) - datetime.timedelta(hours=7)


def main():
    # Load dataset
    columns = ['TWEET_SENTIMENT', 'TWEET_ID', 'TWEET_DATE', 'TWEET_QUERY',
               'TWEET_USER', 'TWEET_CONTENT']
    df = pd.read_csv(
        ppj('OUT_DATA_RAW', 'stanford_twitter_sentiment_corpus.csv'),
        encoding='latin1', names=columns, parse_dates=[2],
        date_parser=dateparse)

    # Drop query (is ``no query``)
    df.drop(['TWEET_QUERY', 'TWEET_USER', 'TWEET_DATE'], axis=1, inplace=True)

    # Drop duplicates which have been tagged twice and sometimes different
    df.drop_duplicates('TWEET_ID', keep=False, inplace=True)

    # Construct dummies for sentiment
    df.TWEET_SENTIMENT.replace({0: 0, 4: 1}, inplace=True)
    df.TWEET_SENTIMENT = df.TWEET_SENTIMENT.astype('category')
    df.TWEET_SENTIMENT.cat.rename_categories(
        ['NEGATIVE', 'POSITIVE'], inplace=True)

    # Save dataset
    joblib.dump(
        df, filename=ppj('OUT_DATA_PROCESSED', 'twitter_stanford.p.lzma'),
        compress=('lzma', 3))


if __name__ == '__main__':
    main()
