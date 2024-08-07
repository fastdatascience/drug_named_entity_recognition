'''
MIT License

Copyright (c) 2023 Fast Data Science Ltd (https://fastdatascience.com)

Maintainer: Thomas Wood

Tutorial at https://fastdatascience.com/drug-named-entity-recognition-python-library/

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

import re
import time

import requests
from lxml import etree

response = requests.get('https://www.nhs.uk/medicines/')

tree = etree.HTML(response.text)

outgoing_links = tree.xpath("//a[contains(@href,'/medicines/')]")

links_to_follow = []

for link in outgoing_links:
    if "medicines/#" not in link.attrib["href"]:
        drug_name = link.text.strip()
        drug_name = re.sub(r'\s+', ' ', drug_name)
        if link.attrib["href"].startswith("http"):
            absolute_url = link.attrib["href"]
        else:
            absolute_url = 'https://www.nhs.uk' + link.attrib["href"]
        links_to_follow.append([absolute_url, drug_name])

# # Download all drug pages

for medicine_page_url, drug_name in links_to_follow:
    words = len(drug_name.split(" "))
    print(medicine_page_url, drug_name)
    page_url_hash = re.sub(r'.+/medicines/|/$', '', medicine_page_url).lower()
    page_url_hash = re.sub(r'[^a-z0-9]+', '-', page_url_hash)
    response = requests.get(medicine_page_url)

    with open("nhs_pages/" + page_url_hash + ".html", "w", encoding="utf-8") as f:
        f.write(medicine_page_url + "\n" + drug_name + "\n" + response.text)

    time.sleep(10)
