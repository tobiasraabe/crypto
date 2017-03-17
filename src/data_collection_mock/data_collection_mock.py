#!/usr/bin/env python

"""This module is for speeding up the data_collection process by using static
files.

"""


import os
import shutil
import yaml
import zipfile

from bld.project_paths import project_paths_join as ppj


def main():
        # Load previously created twitter files
    files = [ppj('IN_STATIC', f) for f in os.listdir(ppj('IN_STATIC'))
             if os.path.isfile(ppj('IN_STATIC', f)) &
             (not f.endswith('.zip'))]
    for file in files:
        print('Moved static file {}.'.format(file))
        shutil.copy2(file, ppj('OUT_DATA_RAW'))

    with open(ppj('IN_DATA_COLLECTION_MOCK', 'mock.yml')) as file:
        mock_config = yaml.load(file.read())

    for query, until in mock_config:
        with open(ppj('OUT_DATA_RAW', 'twitter_{}.yml'
                      .format(query)), 'w') as file:
            yaml.dump({'until': until}, file)

    # Load Stanfords twitter sentiment corpus
    path_stanford = ppj(
        'IN_STATIC', 'stanford_twitter_sentiment_corpus.zip')
    with zipfile.ZipFile(path_stanford, 'r') as zfile:
        zfile.extract(
            'training.1600000.processed.noemoticon.csv',
            ppj('OUT_DATA_RAW'))

    os.rename(
        ppj('OUT_DATA_RAW', 'training.1600000.processed.noemoticon.csv'),
        ppj('OUT_DATA_RAW', 'stanford_twitter_sentiment_corpus.csv'))
    print('Moved static file {}.'
          .format(ppj('IN_STATIC', 'stanford_twitter_sentiment_corpus.zip')))


if __name__ == '__main__':
    main()
