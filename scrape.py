from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import NavigableString
import requests
import re
from collections import *

def is_all_spaces(s):
    return len(s.lstrip()) == 0 or s.lstrip().find('(') == 0

def num_leading_spaces(s):
    return len(s) - len(s.lstrip())

def format_char_name(s):
    paren_index = s.find('(')
    if paren_index > 0:
        return s[:paren_index].strip()
    return s.strip()

# Determine the number of leading spaces before 'dialogue' lines
def get_dialogue_leading_spaces(script):
    nls = []
    for item in script.contents:
        if type(item) != Tag:
            for line in item.split('\n'):
                if not is_all_spaces(line):
                    nls += [num_leading_spaces(line)]

    max_num_spaces = 0
    c = Counter(nls)
    for num_spaces in c:
        if c[num_spaces] > 100:
            max_num_spaces = max(max_num_spaces, num_spaces)
    return max_num_spaces

# Really mediocre initial scraping code
url = 'http://www.imsdb.com/scripts/Buffy-the-Vampire-Slayer.html'
char_lines = {}

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html5lib')
# Different scripts have different amounts of 'pre' tags... >:(
# TODO figure this out automatically
script = soup.find('pre')
if script.find('pre') is not None:
    script = script.find('pre')
nls_dialogue = get_dialogue_leading_spaces(script)
print(nls_dialogue)

current_person = ''
for item in script.contents:
    # Figure out who says a line
    if type(item) == Tag:
        char_name = format_char_name(item.text)
        if len(char_name) > 0:
            current_person = char_name
    else:
        actual_text = ''
        text_lines = item.split('\n')
        for line in text_lines:
            nls_line = num_leading_spaces(line)
            if nls_line == nls_dialogue:
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
