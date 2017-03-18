#!/usr/bin/env python

"""This script downloads all necessary files to the specific folders.

"""

import os
import urllib.request
import zipfile


URL = (
    'https://www.dropbox.com/sh/zj5djqsum7dzrqp/AABKD3nb5WfKn0h'
    '-GtvvFpD7a?dl=1')
PATH_STATIC = os.path.join('src', 'static')
PATH_DOWNLOAD = os.path.join('src', 'static', 'statics.zip')


def download_data():
    request = urllib.request.urlopen(URL)
    data = request.read()
    request.close()

    with open(PATH_DOWNLOAD, 'wb') as f:
        f.write(data)


def unzip_data():
    with zipfile.ZipFile(PATH_DOWNLOAD) as zf:
        zf.extractall(PATH_STATIC)


def clean_up():
    os.remove(PATH_DOWNLOAD)


def main():
    download_data()
    unzip_data()
    clean_up()


if __name__ == '__main__':
    main()