from bs4 import BeautifulSoup
from bs4.element import Tag
from bs4.element import NavigableString
import re
from collections import *
from character import Character
from os import path
import os

# Test push
# Rohin has contributed to this!
# Is a string all spaces (ignores parenthesis)
def is_all_spaces(s):
    return len(s.lstrip()) == 0 or s.lstrip().find('(') == 0

def num_leading_spaces(s):
    return len(s) - len(s.lstrip())

# Utility function, is some string a number
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Formats a character name - removes parens and anything in between parens,
# ignores character names that are just numbers
def format_char_name(s):
    paren_index = s.find('(')
    if paren_index > 0:
        return s[:paren_index].strip()
    if is_number(s.strip()):
        return ''
    return s.strip()

# Determine the number of leading spaces before 'dialogue' lines
def get_dialogue_leading_spaces(script):
    nls = []

    # Count every number of every length of leading spaces
    for item in script.contents:
        if type(item) != Tag:
            for line in item.split('\n'):
                if not is_all_spaces(line):
                    nls += [num_leading_spaces(line)]

    # Determine the number of spaces before the most indented type of line
    max_num_spaces = 0
    c = Counter(nls)
    for num_spaces in c:
        # Make sure this number of spaces occurs enough, so that we're not
        # picking something like right-aligned text at the beginning of a script
        if c[num_spaces] > 100:
            max_num_spaces = max(max_num_spaces, num_spaces)
    return max_num_spaces

def all_words_in(bloblist):
    words = set().union(*[blob.words for blob in bloblist])
    return words

def print_cos_sim(characters):
    bloblist = [char.blob for char in characters]
    all_words = all_words_in(bloblist)
    for char in characters:
        char.gen_tf_idf_vec(bloblist, all_words)
        print(char.name)

    for c1 in characters:
        print('\n========== ' + c1.name + ' ==========')
        cosine_sim = {}
        for c2 in characters:
            cosine_sim[c2.name] = c1.cosine_sim(c2)
        sorted_chars = sorted(characters, key=lambda a : -cosine_sim[a.name])
        for i in range(len(sorted_chars)):
            c2 = sorted_chars[i]

            print((str(i + 1) + '. ' + c2.name).ljust(20) + '{:.4f}'.format(cosine_sim[c2.name]))

def scrape_characters(filepath):
    # Really mediocre initial scraping code
    char_lines = {}

    with open(filepath, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html5lib')
        # find pre tags until we are in the deepest pre tag
        script = soup.find('pre')
        if script is None:
            return []
        while script.find('pre') is not None:
            script = script.find('pre')

        nls_dialogue = get_dialogue_leading_spaces(script)

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
        characters = []
        for char in char_lines:
            if len(char_lines[char]) > 10:
                characters.append(Character(char.title(), char_lines[char]))
        return characters

files = [f for f in os.listdir('./scripts/')]
characters = []
for file in files:
    characters += scrape_characters('./scripts/' + file)

print(len(characters))
#print_cos_sim(characters)
