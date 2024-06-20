import re
import time

import requests
from lxml import etree

response = requests.get('https://www.nhs.uk/medicines/insulin/')

tree = etree.HTML(response.text)

outgoing_links = tree.xpath("//a[contains(@href,'/medicines/')]")

links_to_follow = []

for link in outgoing_links:
    if "medicines/#" not in link.attrib["href"] and "/insulin/" in link.attrib["href"]:
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