#!/usr/bin/env python

import shutil
import os
import yaml
from bld.project_paths import project_paths_join as ppj


PATH_STATIC = os.path.join('..', 'static')


if __name__ == '__main__':
    # Static files
    # Use static files to speed up the data collection process
    files = [os.path.join(PATH_STATIC, f) for f in os.listdir(PATH_STATIC)
             if os.path.isfile(os.path.join(PATH_STATIC, f))]
    for file in files:
        print('Moved static file {}.'.format(file))
        shutil.copy2(file, ppj('OUT_DATA_RAW'))

    with open(ppj('IN_DATA_COLLECTION_MOCK', 'mock.yml')) as file:
        mock_config = yaml.load(file.read())

    for query, until in mock_config:
        with open(ppj('OUT_DATA_RAW', 'twitter_{}.yml'
                      .format(query)), 'w') as file:
            yaml.dump({'until': until}, file)
