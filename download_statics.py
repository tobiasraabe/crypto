#!/usr/bin/env python

"""This script downloads all necessary files to the specific folders.

"""

import urllib.request
import zipfile


URL = 'https://www.dropbox.com/sh/zj5djqsum7dzrqp/AABKD3nb5WfKn0h-GtvvFpD7a?dl=0'


def download_data():
    u = urllib.request.urlopen(url)
    data = u.read()
    u.close()

    with open('statics.zip', 'wb') as f:
        f.write(data)


def unzip_data():
    with zipfile.ZipFile(os.path.join('statics.zip')) as zf:
        zf.extractall(os.path.join('src', 'statics'))


def clean_up():
    os.remove(os.path.join('statics.zip'))


def main():
    download_data()
    unzip_data()
    clean_up()


if __name__ == '__main__':
    main()