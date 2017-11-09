from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import NavigableString
import requests
import re
from collections import *

from scrape import scrape_movie_page

all_movies_url = 'http://www.imsdb.com/all%20scripts/'
all_movies_page = requests.get(all_movies_url).text

soup = BeautifulSoup(all_movies_page, 'html5lib')

links = soup.find_all('table')[1].find_all('a')
movie_pages = []

for link in links:
    if 'Movie Scripts' in link.get('href'):
        movie_pages.append(link.get('href'))

base_link = 'http://www.imsdb.com'
script_links = set()

for page in movie_pages:
    page_link = base_link + page.replace(' ', '%20')
    print(page_link)
    page_response = requests.get(page_link)
    soup = BeautifulSoup(page_response.text, 'html5lib')
    sub_links = soup.find_all('a')
    for link in sub_links:
        if link != None and link.get('href') != None and 'scripts/' in link.get('href'):
            script_links.add(base_link + link.get('href'))
            break

f = open('script_links.txt', 'w')
for script_link in script_links:
    f.write(script_link + '\n')
f.close()