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

import bz2
import csv
import json
import pathlib
import pickle as pkl
import re

from nltk.corpus import words

from inclusions import common_english_words_to_include_in_drugs_dictionary, \
    extra_terms_to_exclude_from_drugs_dictionary, extra_mappings, drugs_to_exclude_under_all_variants

re_num = re.compile(r'^\d+$')
re_three_digits = re.compile(r'\d\d\d')

this_path = pathlib.Path(__file__).parent.resolve()

drug_variant_to_canonical = {}
drug_canonical_to_data = {}
drug_variant_to_variant_data = {}

with open("mesh_name_to_smiles.json", "r", encoding="utf-8") as f:
    mesh_lc_name_to_smiles = json.loads(f.read())

with open("mesh_name_to_mass.json", "r", encoding="utf-8") as f:
    mesh_lc_name_to_mass = json.loads(f.read())


def add_canonical(canonical: str, data: dict):
    canonical_norm = canonical.lower().strip()
    if canonical_norm in drug_variant_to_canonical and canonical_norm not in drug_variant_to_canonical[canonical_norm]:
        print(f"Adding canonical {canonical_norm} but it already maps to {drug_variant_to_canonical[canonical_norm]}")
        canonical_norm = drug_variant_to_canonical[canonical_norm][0]
    elif canonical_norm not in drug_variant_to_canonical:
        data["name"] = canonical
    if canonical_norm not in drug_canonical_to_data:
        drug_canonical_to_data[canonical_norm] = data
    else:
        drug_canonical_to_data[canonical_norm] = drug_canonical_to_data[canonical_norm] | data


def add_synonym(synonym: str, canonical: str, synonym_data: dict = None):
    canonical_norm = canonical.lower().strip()
    synonym_norm = synonym.lower().strip()
    if synonym_norm not in drug_variant_to_canonical:
        drug_variant_to_canonical[synonym_norm] = [canonical_norm]
    else:
        if canonical_norm not in drug_variant_to_canonical:
            drug_variant_to_canonical[synonym_norm].append(canonical_norm)
    if synonym_data is not None:
        if synonym_norm not in drug_variant_to_variant_data:
            drug_variant_to_variant_data[synonym_norm] = synonym_data
        else:
            drug_variant_to_variant_data[synonym_norm] = drug_variant_to_variant_data[synonym_norm] | synonym_data


with open(this_path.joinpath("drugs_dictionary_medlineplus.csv"), 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in csv_reader:
        if not headers:
            headers = row
            continue
        id = row[0]
        canonical = row[1]
        synonyms = row[2].split("|")

        canonical = re.sub(
            r"(?i) (Injection|Oral Inhalation|Transdermal|Ophthalmic|Topical|Vaginal Cream|Nasal Spray|Transdermal Patch|Rectal)",
            "", canonical)

        add_canonical(canonical, {"medline_plus_id": id})
        add_synonym(canonical, canonical, {"is_brand": False})
        for synonym in synonyms:
            add_synonym(synonym, canonical)

with open("all_nhs_drugs.json", "r", encoding="utf-8") as f:
    nhs_data = json.loads(f.read())


def get_names_nhs(text: str):
    possible_names = re.split(r"[,\(]", text)

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


def get_brand_names_nhs(description: str):
    if "brand name" in description.lower():
        description = description.strip()
        description = re.sub(r'(?i)\W*brand names?\W*', '', description)
        description = re.sub(r'(?i)find out.*', '', description)
        return get_names_nhs(description)
    return []


for nhs_drug in nhs_data:
    names = get_names_nhs(nhs_drug["name"])
    brand_names = get_brand_names_nhs(nhs_drug["description"])

    nhs_website_url = re.sub(".+nhs.uk/nhs-website-content", "https://nhs.uk", nhs_drug["url"])
    data = {"nhs_api_url": nhs_drug["url"], "nhs_url": nhs_website_url}
    canonical = names[0]
    add_canonical(canonical, data)
    add_synonym(canonical, canonical, {"is_brand": False})
    if len(names) > 1:
        for synonym in names[1:]:
            add_synonym(synonym, canonical)
    for synonym in brand_names:
        add_synonym(synonym, canonical, {"is_brand": True})

with open(this_path.joinpath("drugs_dictionary_mesh.csv"), 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in csv_reader:
        if not headers:
            headers = row
            continue
        id = row[0]
        generic_names = row[1].split("|")
        common_name = row[2]
        synonyms = row[3].split("|")
        tree = row[4].split("|")
        data = {"mesh_id": id, "mesh_tree": tree}

        canonical = common_name

        add_canonical(canonical, data)
        for synonym in generic_names:
            add_synonym(synonym, canonical, {"is_brand": False})
        add_synonym(common_name, canonical)
        for synonym in synonyms:
            add_synonym(synonym, canonical)

print(
    f"Added MeSH data.")

with open(this_path.joinpath("drugbank vocabulary.csv"), 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in csv_reader:
        if not headers:
            headers = row
            continue
        id = row[0]
        data = {"drugbank_id": id}
        canonical = row[2]
        synonyms = row[5].split("|")

        add_canonical(canonical, data)
        add_synonym(canonical, canonical)
        for synonym in synonyms:
            add_synonym(synonym, canonical)

with open(this_path.joinpath("drugs_dictionary_wikipedia.csv"), 'r', encoding="utf-8") as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=',')
    headers = None
    for row in csv_reader:
        if not headers:
            headers = row
            continue
        wikipedia_url = row[0]
        data = {"wikipedia_url": wikipedia_url}
        canonical = row[1]
        canonical = re.sub(r' \(medication.+', '', canonical)
        synonyms = row[2].split("|")

        add_canonical(canonical, data)
        add_synonym(canonical, canonical)
        for synonym in synonyms:
            add_synonym(synonym, canonical)

for surface_form, canonical_form in extra_mappings.items():
    add_synonym(surface_form, canonical_form)

# Add SMILES and mass data

number_of_smiles_matches_found = 0
number_of_smiles_matches_not_found = 0

for drug_variant, canonical in drug_variant_to_canonical.items():
    tmp_name_to_lookup_smiles_lc = drug_variant.lower()
    for ctr in range(3):
        if canonical[0] in drug_variant_to_canonical:
            canonical = drug_variant_to_canonical[canonical[0]]
    data = drug_canonical_to_data[canonical[0]]
    if tmp_name_to_lookup_smiles_lc in mesh_lc_name_to_smiles:
        data["smiles"] = mesh_lc_name_to_smiles[tmp_name_to_lookup_smiles_lc]
    if tmp_name_to_lookup_smiles_lc in mesh_lc_name_to_mass:
        data["formula"] = mesh_lc_name_to_mass[tmp_name_to_lookup_smiles_lc][0]
        data["mass_lower"] = mesh_lc_name_to_mass[tmp_name_to_lookup_smiles_lc][1]
        data["mass_upper"] = mesh_lc_name_to_mass[tmp_name_to_lookup_smiles_lc][2]
    if "smiles" in data:
        number_of_smiles_matches_found += 1
    else:
        number_of_smiles_matches_not_found += 1

print(
    f"We were able to match the MeSH names to {number_of_smiles_matches_found} SMILES strings but {number_of_smiles_matches_not_found} could not be matched to SMILES.")

# Remove common English words

print("Finding all drugs that are also in the NLTK list of English words.")

all_english_vocab = set([w.lower() for w in words.words()])

words_to_check_with_ai = set()
for word in list(drug_variant_to_canonical):
    reason = None
    if word in all_english_vocab and word not in common_english_words_to_include_in_drugs_dictionary:
        reason = "it is an English word in NLTK dictionary"
        if word not in common_english_words_to_include_in_drugs_dictionary and len(word) > 2:
            words_to_check_with_ai.add(word)
    elif word in extra_terms_to_exclude_from_drugs_dictionary:
        reason = "it is in the manual ignore list"
    elif len(word) < 4 and word not in common_english_words_to_include_in_drugs_dictionary:
        reason = "it is short"
    elif len(re_num.findall(word)) > 0:
        reason = "it is numeric"
    elif len(word) > 50:
        reason = "it is too long"
    elif "(" in word or "//" in word:
        reason = "it contains forbidden punctuation"
    elif len(re_three_digits.findall(word)) > 0:
        reason = "it contains 3 or more consecutive digits"
    if reason is not None:
        print(f"Removing [{word}] from drug dictionary because {reason}")
        del drug_variant_to_canonical[word]

canonical_has_variants_pointing_to_it = set()
for variant, canonicals in drug_variant_to_canonical.items():
    for canonical in canonicals:
        canonical_has_variants_pointing_to_it.add(canonical)

with open("words_to_check_with_ai.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(sorted(words_to_check_with_ai)))

# Find any redirects that go through twice

all_redirects_fixed = set()
for i in range(3):
    print(f"Normalising redirects step {i}")
    redirects_needed = {}
    for variant, canonicals in list(drug_variant_to_canonical.items()):
        for canonical in canonicals:
            if canonical in drug_variant_to_canonical:
                for canonical_of_canonical in drug_variant_to_canonical[canonical]:
                    if canonical_of_canonical != canonical:
                        redirects_needed[variant] = drug_variant_to_canonical[canonical]
                        all_redirects_fixed.add(variant)
    print(f"There are {len(redirects_needed)} drug names which are redirected twice. These need to be normalised")
    for source, targets in redirects_needed.items():
        drug_variant_to_canonical[source] = targets

for variant in all_redirects_fixed:
    canonicals = drug_variant_to_canonical[variant]
    for canonical in canonicals:
        synonyms = set(drug_canonical_to_data[canonical].get("synonyms", []))
        if variant not in synonyms:
            print(f"Variant {variant} not listed as synonym of {canonical}. Adding it")
            synonyms.add(variant)
            drug_canonical_to_data[canonical]["synonyms"] = sorted(synonyms)

# Remove any entries in the database that will never be used because nothing points there

for canonical in list(drug_canonical_to_data):
    if canonical not in canonical_has_variants_pointing_to_it:
        print(f"removing data for {canonical} because there are no synonyms pointing to it")
        del drug_canonical_to_data[canonical]

# Hard delete some terms in all variants e.g. blood glucose
inverted_index_lookup_canonical_to_variants = dict()
for variant, canonicals in drug_variant_to_canonical.items():
    for canonical in canonicals:
        if canonical not in inverted_index_lookup_canonical_to_variants:
            inverted_index_lookup_canonical_to_variants[canonical] = set()
        inverted_index_lookup_canonical_to_variants[canonical].add(variant)

for term_to_delete in drugs_to_exclude_under_all_variants:
    variants = inverted_index_lookup_canonical_to_variants[term_to_delete]
    for variant in variants:
        del drug_variant_to_canonical[variant]
    del drug_canonical_to_data[term_to_delete]

with bz2.open("../src/drug_named_entity_recognition/drug_ner_dictionary.pkl.bz2", "wb") as f:
    pkl.dump(
        {"drug_variant_to_canonical": drug_variant_to_canonical,
         "drug_canonical_to_data": drug_canonical_to_data,
         "drug_variant_to_variant_data": drug_variant_to_variant_data},
        f
    )
