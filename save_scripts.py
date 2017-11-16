import json
import requests
from urllib import pathname2url
with open('script_links.json', 'r') as f:
    script_list = json.loads(f.read())

    for script in script_list:
        name = script['name']
        url = script['url']
        print(name, url)
        if url[-5:] != '.html':
            continue
        response = requests.get(url)
        with open('./scripts/' + pathname2url(name.replace(' ', '_')) + '.html', 'w') as script_file:
            script_file.write(response.text.encode('utf-8'))