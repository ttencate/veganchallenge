#!/usr/bin/python3

import os
import urllib.request

from bs4 import BeautifulSoup

def cached_fetch(url, cache_key, postdata=None):
    try:
        with open(cache_key, 'rb') as in_file:
            return in_file.read()
    except Exception as ex:
        if postdata is not None and postdata is not bytes:
            postdata = bytes(postdata, 'utf-8')
        with urllib.request.urlopen(url, postdata) as in_url:
            data = in_url.read()
        with open(cache_key, 'wb') as out_file:
            out_file.write(data)
        return data

for date in [
        '2017-03-27',
        '2017-04-03',
        '2017-04-10',
        '2017-04-17',
        '2017-04-24',
        ]:
    week = cached_fetch('https://veganchallenge.nl/getmenu/', '%s.html' % date, 'date=%s' % date)
    soup = BeautifulSoup(week, 'html.parser')
    print(soup.prettify())
