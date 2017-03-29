#!/usr/bin/python3

import os
import os.path
import sys
import urllib.request

from bs4 import BeautifulSoup

def cached_fetch(url, cache_key, postdata=None):
    cache_file = os.path.join('cache', cache_key)
    try:
        with open(cache_file, mode='rb') as in_file:
            return in_file.read()
    except Exception as ex:
        print('Fetching %s...' % url, file=sys.stderr)
        if postdata is not None and postdata is not bytes:
            postdata = bytes(postdata, 'utf-8')
        with urllib.request.urlopen(url, postdata) as in_url:
            data = in_url.read()
        with open(cache_file, mode='wb') as out_file:
            out_file.write(data)
        return data

def tex_encode(s):
    return s.replace('&', '\\&')

def process_recipe(name, url):
    recipe = cached_fetch(url, '%s.html' % name).decode('utf-8')
    soup = BeautifulSoup(recipe, 'html.parser')

    title = soup.find('h1').text.strip()
    intro = soup.find('h1').parent
    intro.find('h1').extract()
    summary = intro.text.strip()
    ingredienten, bereiding = [h2.parent for h2 in soup.find_all('h2', class_='recipetitle')]

    picture_url = soup.find(class_='wp-post-image')['src']
    picture_name = picture_url.split('/')[-1].replace('_', '-')
    picture_data = cached_fetch(picture_url, picture_name)
    with open(os.path.join('pictures', picture_name), mode='wb') as out_picture:
        out_picture.write(picture_data)

    ingredients = [li.text.strip() for li in ingredienten.find_all('li')]
    ingredients = [ingredient for ingredient in ingredients if ingredient]
    bereiding.find('h2').extract()
    directions = bereiding.text.strip()

    with open(os.path.join('include', '%s.tex' % name), mode='wt', encoding='utf-8') as out_recipe:
        out_recipe.write('\\begin{recipe}\n')
        out_recipe.write('%% %s\n' % url)
        out_recipe.write('\n')

        out_recipe.write('\\recipepicture{pictures/%s}\n' % picture_name)

        out_recipe.write('\\recipetitle{%s}\n' % tex_encode(title))

        out_recipe.write('\\begin{recipesummary}\n')
        out_recipe.write('%s\n' % tex_encode(summary))
        out_recipe.write('\\end{recipesummary}\n')
        out_recipe.write('\n')

        out_recipe.write('\\begin{ingredients}\n')
        for ingredient in ingredients:
            out_recipe.write('\\ingredient{%s}\n' % tex_encode(ingredient))
        out_recipe.write('\\end{ingredients}\n')
        out_recipe.write('\n')

        out_recipe.write('\\begin{directions}\n')
        out_recipe.write('%s\n' % tex_encode(directions))
        out_recipe.write('\\end{directions}\n')
        out_recipe.write('\n')

        out_recipe.write('\\end{recipe}\n')

with open(os.path.join('include', 'dagmenus.tex'), mode='wt', encoding='utf-8') as out_dagmenus:
    for date in [
            '2017-03-27',
            '2017-04-03',
            '2017-04-10',
            '2017-04-17',
            '2017-04-24',
            ]:
        week = cached_fetch('https://veganchallenge.nl/getmenu/', '%s.html' % date, 'date=%s' % date).decode('utf-8')
        soup = BeautifulSoup(week, 'html.parser')
        for dagmenu in soup.find_all(class_='_dagmenu'):

            h2 = dagmenu.find('h2')
            if not h2:
                continue
            day = h2.text.rstrip(':').replace('  ', ' ').capitalize()
            print('# %s' % day)

            out_dagmenus.write('\\begin{dagmenu}{%s}\n' % tex_encode(day))

            for receptitem in dagmenu.find_all(class_='receptitem'):
                meal = receptitem.find(class_='headtitle').text.capitalize()
                title = receptitem.find(class_='title').text
                url = receptitem.find(class_='title').find('a')['href']
                name = url.split('/')[-2]
                print('%s: %s (%s)' % (meal, title, url))

                out_dagmenus.write('\\includerecipe{%s}{include/%s.tex}\n' % (meal, name))

                process_recipe(name, url)

            print()

            out_dagmenus.write('\\end{dagmenu}\n')
            out_dagmenus.write('\n')
