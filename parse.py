#!/usr/bin/python3

import os
import urllib.request

from bs4 import BeautifulSoup

def cached_fetch(url, cache_key, postdata=None):
    try:
        with open(cache_key, mode='r', encoding='utf-8') as in_file:
            return in_file.read()
    except Exception as ex:
        print('Fetching %s...' % url)
        if postdata is not None and postdata is not bytes:
            postdata = bytes(postdata, 'utf-8')
        with urllib.request.urlopen(url, postdata) as in_url:
            data = in_url.read().decode('utf-8')
        with open(cache_key, mode='w', encoding='utf-8') as out_file:
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
    for dagmenu in soup.find_all(class_='_dagmenu'):
        h2 = dagmenu.find('h2')
        if not h2:
            continue
        day = h2.text.rstrip(':').replace('  ', ' ').capitalize()
        print('# %s' % day)
        for receptitem in dagmenu.find_all(class_='receptitem'):
            meal = receptitem.find(class_='headtitle').text.capitalize()
            title = receptitem.find(class_='title').text
            print('%s: %s' % (meal, title))
        print()