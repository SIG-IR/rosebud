from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import NavigableString
import requests
import re

# Really mediocre initial scraping code
url = 'http://www.imsdb.com/scripts/Blade-Runner.html'
# Indentation for dialogue, in spaces - TODO automatically figure this out
line_str = '                  '
line_str_len = len(line_str)
char_lines = {}

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html5lib')
# Different scripts have different amounts of 'pre' tags... >:(
# TODO figure this out automatically
script = soup.find('pre').find('pre')

current_person = ''
for item in script.contents:
    # Figure out who says a line
    if type(item) == Tag:
        tag_text = item.text.strip()
        if len(tag_text) > 0:
            current_person = tag_text
    else:
        actual_text = ''
        text_lines = item.split('\n')
        for line in text_lines:
            if len(line) > line_str_len and line[:line_str_len] == line_str:
                actual_text += ' ' + line.strip()
        # Remove extraneous spaces
        actual_text = re.sub(' +', ' ', actual_text).strip()
        if len(actual_text) > 0:
            # Add to character's lines
            if current_person not in char_lines:
                char_lines[current_person] = []
            char_lines[current_person].append(actual_text)

for char in char_lines:
    print(str(len(char_lines[char])) + '\t' +char)
