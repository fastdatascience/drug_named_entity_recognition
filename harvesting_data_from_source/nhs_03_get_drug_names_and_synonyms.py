import csv
import os
import re

from lxml import html

input_folder = "nhs_pages/"


def get_names(text: str):
    possible_names = re.split("[,\(]", text)

    names_found = list()
    for name in possible_names:
        name = re.sub(r'\)|,', '', name).strip()
        name = re.sub(r'^(?:rectal|oral|vaginal|.*-acting)\b', '', name).strip()
        name = re.sub(
            r'\b(?:rectal foam and enemas|for (?:adults|children|skin|eyes|depression|piles|pain|migraine|thrush|mouth|type|gestational).*|gels?|rectal foams?|nasal sprays?|pain and migraine|tablets?|tablets and liquid|creams?|skin creams?)$',
            '', name)
        name = name.strip()
        name = re.sub(r'\.$', '', name)
        names_found.append(name)

    return names_found


rows = []
for root, folder, files in os.walk(input_folder):
    for file_name in files:

        if not file_name.endswith("html"):
            continue

        full_file = input_folder + "/" + file_name
        with open(full_file, "r", encoding="utf-8") as f:
            url = f.readline().strip()
            content = f.read()
        url = re.sub('/$', '', url)

        tree = html.fromstring(content)

        name_from_h1 = tree.xpath("//h1")[0].text.strip()

        spans = tree.xpath("//h1/span")
        if len(spans) > 0:
            name = spans[0].text.strip()

        name_from_anchor_text = content.split("\n")[0]
        if name != name_from_anchor_text:
            print(f"Name mismatch: [{name}] , [{name_from_anchor_text}]")

        brand_names = tree.xpath("//span[contains(text(), 'rand name')]")

        brand_names.extend(tree.xpath("//p[contains(text(), 'rand name')]"))

        brand_names.extend(tree.xpath("//span[contains(text(), 'rand Name')]"))
        brand_names.extend(tree.xpath("//p[contains(text(), 'rand Name')]"))

        confirmed_brand_names = []
        for n in brand_names:
            text = n.text_content().strip()
            text = re.sub('(?i)\W*brand names?\W*', '', text)
            text = re.sub('(?i)find out.*', '', text)
            confirmed_brand_names.extend(get_names(text))

        canonical_names = get_names(name_from_anchor_text)
        canonical_names.extend(get_names(name_from_h1))
        canonical_names.extend(confirmed_brand_names)

        name = canonical_names[0]

        synonyms = set(canonical_names[1:])
        if "" in synonyms:
            synonyms.remove("")

        synonyms = "|".join(synonyms)

        cols = [url, name, synonyms]

        rows.append(cols)

# Sort the rows from shortest to longest URL
rows = sorted(rows, key=lambda x: len(x[0]))

with open("drugs_dictionary_nhs.csv", "w", encoding="utf-8") as fo:
    writer = csv.writer(fo)
    writer.writerow(["NHS link", "Common name", "Synonyms"])

    for cols in rows:
        writer.writerow(cols)
