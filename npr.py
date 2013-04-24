#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Copyright (C) 2013 by Lele Long <schemacs@gmail.com>
This file is free software, distributed under the GPL License.

Download the latest three episodes for npr hourly news.

http://pymotw.com/2/xml/etree/ElementTree/parse.html

'''
import xml.etree.ElementTree as ET
import urllib
import os
import re
from dateutil import parser
import datetime


NS_MAP = dict(itunes="http://www.itunes.com/dtds/podcast-1.0.dtd")
BASE_DIR = '~/Downloads/cron/cbs'

def download_hook(block_count, block_size, length):
    progress = 100.0 * block_count * block_size / length
    if int(progress) % 11 == 1:
        if progress > 100:
            progress = 100.0
        print '{0:.2f}%'.format(progress)


def get_filepath(title):
    match = re.match(r'NPR News: (.*)', title)
    try:
        dt = parser.parse(match.group(1))
    except Exception as ex:
        print "parse failed, return NOW()", ex
        dt = datetime.datetime.now()
    return os.path.expanduser(os.path.join(BASE_DIR, '%d.mp3' % (dt.hour % 3)))


def hourlynews():
    url = 'http://www.npr.org/rss/podcast.php?id=500005'
    try:
        fh = urllib.urlopen(url)
    except Exception as e:
        print e
        return
    root = ET.fromstring(fh.read())
    channel = root.find('channel')
    item = channel.find('item')
    title = item.find('description').text
    audio_url = None
    enclosure = item.find('enclosure')
    if enclosure is not None:
        audio_url = enclosure.get('url', None)
    #length = item.find('enclosure').get('length')
    #audio_type = item.find('enclosure').get('type')
    #print item.find('itunes:keywords', NS_MAP).text
    #print item.find('itunes:duration', NS_MAP).text
    #filename = os.path.basename(audio_url)
    filename = get_filepath(title)
    if audio_url:
        urllib.urlretrieve(audio_url, filename, download_hook)


def main():
    #print get_filepath('NPR News: 03-03-2013 7AM ET')
    hourlynews()


if __name__ == "__main__":
    main()
