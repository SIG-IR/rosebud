from bs4 import BeautifulSoup
import requests
import json

all_movies_url = 'http://www.imsdb.com/all%20scripts/'
all_movies_page = requests.get(all_movies_url).text

soup = BeautifulSoup(all_movies_page, 'html5lib')

links = soup.find_all('table')[1].find_all('a')
movie_pages = []

for link in links:
    if 'Movie Scripts' in link.get('href'):
        movie_pages.append((link.text.strip(), link.get('href')))

base_link = 'http://www.imsdb.com'
script_links = set()

for page in movie_pages:
    page_link = base_link + page[1].replace(' ', '%20')
    print(page_link)
    page_response = requests.get(page_link)
    soup = BeautifulSoup(page_response.text, 'html5lib')
    sub_links = soup.find_all('a')
    for link in sub_links:
        if link != None and link.get('href') != None and 'scripts/' in link.get('href'):
            script_links.add((page[0], base_link + link.get('href')))

with open('script_links.json', 'w') as f:
    movie_objs = [{'name': link[0], 'url': link[1]} for link in script_links]
    f.write(json.dumps(movie_objs))