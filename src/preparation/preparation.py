#!/usr/bin/env python

"""This module is for speeding up the data_collection process by using static
files.

"""


import os
import shutil
import zipfile

from bld.project_paths import project_paths_join as ppj


PATH_STATIC_STANFORD = ppj(
    'IN_STATIC', 'stanford_twitter_sentiment_corpus.zip')
PATH_DATA_RAW_STANFORD = ppj(
    'OUT_DATA_RAW', 'stanford_twitter_sentiment_corpus.csv')


def main():
        # Load previously created twitter files
    files = [ppj('IN_STATIC', f) for f in os.listdir(ppj('IN_STATIC'))
             if os.path.isfile(ppj('IN_STATIC', f)) &
             (not f.endswith('.zip')) &
             (not f.endswith('.gitkeep'))
             ]
    for file in files:
        shutil.copy2(file, ppj('OUT_DATA_RAW'))
        print('Moved static file {}.'.format(file))

    # Load Stanfords twitter sentiment corpus
    if os.path.isfile(PATH_DATA_RAW_STANFORD):
        pass
    else:
        with zipfile.ZipFile(PATH_STATIC_STANFORD, 'r') as zfile:
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
