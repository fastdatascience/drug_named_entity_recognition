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
import os
import pathlib
import pickle as pkl
from collections import Counter
from drug_named_entity_recognition.structure_file_downloader import download_structures
from drug_named_entity_recognition.util import stopwords
from drug_named_entity_recognition.omop_api import get_omop_id_from_drug
import pickle

# Caching setup
CACHE_FILE = "omop_cache.pkl"
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        omop_cache = pickle.load(f)
else:
    omop_cache = {}

def cached_get_omop_id(drug_name):
    name = drug_name.lower()
    if name in omop_cache:
        return omop_cache[name]
    omop_id = get_omop_id_from_drug(name)
    omop_cache[name] = omop_id
    with open(CACHE_FILE, "wb") as f:
        pickle.dump(omop_cache, f)
    return omop_id

dbid_to_mol_lookup = {}

this_path = pathlib.Path(__file__).parent.resolve()
with bz2.open(this_path.joinpath("drug_ner_dictionary.pkl.bz2"), "rb") as f:
    d = pkl.load(f)

home_path = pathlib.Path.home()
structures_folder = home_path.joinpath(".drug_names")
structures_file = structures_folder.joinpath("open structures.sdf")

drug_variant_to_canonical = {}
drug_canonical_to_data = {}
drug_variant_to_variant_data = {}
ngram_to_variant = {}
variant_to_ngrams = {}

def get_ngrams(text):
    n = 3
    ngrams = set()
    for i in range(0, len(text) - n + 1):
        ngrams.add(text[i:i + n])
    return ngrams

def reset_drugs_data():
    drug_variant_to_canonical.clear()
    drug_canonical_to_data.clear()
    drug_variant_to_variant_data.clear()
    ngram_to_variant.clear()
    variant_to_ngrams.clear()

    drug_variant_to_canonical.update(d["drug_variant_to_canonical"])
    drug_canonical_to_data.update(d["drug_canonical_to_data"])
    drug_variant_to_variant_data.update(d["drug_variant_to_variant_data"])

    for variant, canonicals in drug_variant_to_canonical.items():
        for canonical in canonicals:
            if canonical in drug_canonical_to_data:
                if "synonyms" not in drug_canonical_to_data[canonical]:
                    drug_canonical_to_data[canonical]["synonyms"] = []
                drug_canonical_to_data[canonical]["synonyms"].append(variant)

    for drug_variant in drug_variant_to_canonical:
        ngrams = get_ngrams(drug_variant)
        variant_to_ngrams[drug_variant] = ngrams
        for ngram in ngrams:
            if ngram not in ngram_to_variant:
                ngram_to_variant[ngram] = []
            ngram_to_variant[ngram].append(drug_variant)

def find_drugs(tokens: list, is_fuzzy_match=False, is_ignore_case=None, is_include_structure=False, use_omop_api=False):
    if is_include_structure and len(dbid_to_mol_lookup) == 0:
        dbid_to_mol_lookup["downloading"] = True
        if not os.path.exists(structures_file):
            structures_folder.mkdir(parents=True, exist_ok=True)
            download_structures(structures_folder)

        is_in_structure = True
        current_structure = ""
        with open(structures_file, "r", encoding="utf-8") as f:
            for l in f:
                if is_in_structure and "DRUGBANK_ID" not in l:
                    current_structure += l
                if l.startswith("DB"):
                    dbid_to_mol_lookup[l.strip()] = current_structure
                    current_structure = ""
                    is_in_structure = False
                if l.startswith("$$$$"):
                    is_in_structure = True

    drug_matches = []
    is_exclude = set()

    for token_idx, token in enumerate(tokens[:-1]):
        next_token = tokens[token_idx + 1]
        cand = token + " " + next_token
        cand_norm = cand.lower()
        match = drug_variant_to_canonical.get(cand_norm, None)
        if match:
            for m in match:
                match_data = dict(drug_canonical_to_data.get(m, {})) | drug_variant_to_variant_data.get(cand_norm, {})
                match_data["match_type"] = "exact"
                match_data["matching_string"] = cand
                lookup_name = match_data.get("name") or m
                if use_omop_api:
                    match_data["omop_id"] = cached_get_omop_id(lookup_name)
                drug_matches.append((match_data, token_idx, token_idx + 1))
                is_exclude.update([token_idx, token_idx + 1])

    for token_idx, token in enumerate(tokens):
        if token_idx in is_exclude:
            continue
        cand_norm = token.lower()
        match = drug_variant_to_canonical.get(cand_norm, None)
        if match:
            for m in match:
                match_data = dict(drug_canonical_to_data.get(m, {})) | drug_variant_to_variant_data.get(cand_norm, {})
                match_data["match_type"] = "exact"
                match_data["matching_string"] = token
                lookup_name = match_data.get("name") or m
                if use_omop_api:
                    match_data["omop_id"] = cached_get_omop_id(lookup_name)
                drug_matches.append((match_data, token_idx, token_idx))

    if is_include_structure:
        for match in drug_matches:
            match_data = match[0]
            if "drugbank_id" in match_data:
                structure = dbid_to_mol_lookup.get(match_data["drugbank_id"])
                if structure is not None:
                    match_data["structure_mol"] = structure

    return drug_matches

reset_drugs_data()
