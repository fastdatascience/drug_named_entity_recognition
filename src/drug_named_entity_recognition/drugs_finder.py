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

from drug_named_entity_recognition.omop_api import get_omop_id_from_drug
from drug_named_entity_recognition.structure_file_downloader import download_structures
from drug_named_entity_recognition.util import stopwords

dbid_to_mol_lookup = {}

this_path = pathlib.Path(__file__).parent.resolve()
with bz2.open(this_path.joinpath("drug_ner_dictionary.pkl.bz2"), "rb") as f:
    d = pkl.load(f)

home_path = pathlib.Path.home()
structures_folder = home_path.joinpath(".drug_names")
structures_file = structures_folder.joinpath("open structures.sdf")

# Caching setup
CACHE_FILE = home_path.joinpath(".omop_cache.pkl")
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "rb") as f:
        omop_cache = pkl.load(f)
else:
    omop_cache = {}


def cached_get_omop_id(drug_name):
    name = drug_name.lower()
    if name in omop_cache:
        return omop_cache[name]
    omop_id = get_omop_id_from_drug(name)
    omop_cache[name] = omop_id
    with open(CACHE_FILE, "wb") as f:
        pkl.dump(omop_cache, f)
    return omop_id


drug_variant_to_canonical = {}
drug_canonical_to_data = {}
drug_variant_to_variant_data = {}
ngram_to_variant = {}
variant_to_ngrams = {}


def get_ngrams(text):
    n = 3
    ngrams = set()
    for i in range(0, len(text) - n + 1, 1):
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


def add_custom_drug_synonym(drug_variant: str, canonical_name: str, optional_variant_data: dict = None):
    drug_variant = drug_variant.lower()
    canonical_name = canonical_name.lower()
    drug_variant_to_canonical[drug_variant] = [canonical_name]
    if optional_variant_data is not None and len(optional_variant_data) > 0:
        drug_variant_to_variant_data[drug_variant] = optional_variant_data

    ngrams = get_ngrams(drug_variant)
    variant_to_ngrams[drug_variant] = ngrams
    for ngram in ngrams:
        if ngram not in ngram_to_variant:
            ngram_to_variant[ngram] = []
        ngram_to_variant[ngram].append(drug_variant)

    return f"Added {drug_variant} as a synonym for {canonical_name}. Optional data attached to this synonym = {optional_variant_data}"


def add_custom_new_drug(drug_name, drug_data):
    drug_name = drug_name.lower()
    drug_canonical_to_data[drug_name] = drug_data
    add_custom_drug_synonym(drug_name, drug_name)

    return f"Added {drug_name} to the tool with data {drug_data}"


def remove_drug_synonym(drug_variant: str):
    drug_variant = drug_variant.lower()
    ngrams = get_ngrams(drug_variant)

    del variant_to_ngrams[drug_variant]
    del drug_variant_to_canonical[drug_variant]
    del drug_variant_to_variant_data[drug_variant]

    for ngram in ngrams:
        ngram_to_variant[ngram].remove(drug_variant)

    return f"Removed {drug_variant} from dictionary"


def get_fuzzy_match(surface_form: str):
    query_ngrams = get_ngrams(surface_form)
    candidate_to_num_matching_ngrams = Counter()
    for ngram in query_ngrams:
        candidates = ngram_to_variant.get(ngram, None)
        if candidates is not None:
            for candidate in candidates:
                candidate_to_num_matching_ngrams[candidate] += 1

    candidate_to_jaccard = {}
    for candidate, num_matching_ngrams in candidate_to_num_matching_ngrams.items():
        ngrams_in_query_and_candidate = query_ngrams.union(variant_to_ngrams[candidate])
        jaccard = num_matching_ngrams / len(ngrams_in_query_and_candidate)
        candidate_to_jaccard[candidate] = jaccard

    query_length = len(surface_form)
    if len(candidate_to_num_matching_ngrams) > 0:
        top_candidate = max(candidate_to_jaccard, key=candidate_to_jaccard.get)
        jaccard = candidate_to_jaccard[top_candidate]
        query_ngrams_missing_in_candidate = query_ngrams.difference(variant_to_ngrams[top_candidate])
        candidate_ngrams_missing_in_query = variant_to_ngrams[top_candidate].difference(query_ngrams)

        candidate_length = len(top_candidate)
        length_diff = abs(query_length - candidate_length)
        if max([len(query_ngrams_missing_in_candidate), len(candidate_ngrams_missing_in_query)]) <= 3 \
                and length_diff <= 2:
            return top_candidate, jaccard
    return None, None


def find_drugs(tokens: list, is_fuzzy_match=False, is_ignore_case=None, is_include_structure=False,
               is_use_omop_api=False):
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
                if is_use_omop_api:
                    match_data["omop_id"] = cached_get_omop_id(lookup_name)
                drug_matches.append((match_data, token_idx, token_idx + 2))
            is_exclude.update([token_idx, token_idx + 1])

        elif is_fuzzy_match:
            if token.lower() not in stopwords and next_token.lower() not in stopwords:
                fuzzy_matched_variant, similarity = get_fuzzy_match(cand_norm)
                if fuzzy_matched_variant is not None:
                    match = drug_variant_to_canonical[fuzzy_matched_variant]
                    for m in match:
                        match_data = dict(drug_canonical_to_data.get(m, {})) | drug_variant_to_variant_data.get(
                            fuzzy_matched_variant, {})
                        match_data["match_type"] = "fuzzy"
                        match_data["match_similarity"] = similarity
                        match_data["match_variant"] = fuzzy_matched_variant
                        match_data["matching_string"] = cand
                        if is_use_omop_api:
                            lookup_name = match_data.get("name") or m
                            match_data["omop_id"] = cached_get_omop_id(lookup_name)
                        drug_matches.append((match_data, token_idx, token_idx + 2))
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
                if is_use_omop_api:
                    match_data["omop_id"] = cached_get_omop_id(lookup_name)
                drug_matches.append((match_data, token_idx, token_idx + 1))
                is_exclude.add(token_idx)
        elif is_fuzzy_match:
            if cand_norm not in stopwords and len(cand_norm) > 3:
                fuzzy_matched_variant, similarity = get_fuzzy_match(cand_norm)
                if fuzzy_matched_variant is not None:
                    match = drug_variant_to_canonical[fuzzy_matched_variant]
                    for m in match:
                        match_data = dict(drug_canonical_to_data.get(m, {})) | drug_variant_to_variant_data.get(
                            fuzzy_matched_variant, {})
                        match_data["match_type"] = "fuzzy"
                        match_data["match_similarity"] = similarity
                        match_data["match_variant"] = fuzzy_matched_variant
                        match_data["matching_string"] = token
                        lookup_name = match_data.get("name") or m
                        if is_use_omop_api:
                            match_data["omop_id"] = cached_get_omop_id(lookup_name)
                        drug_matches.append((match_data, token_idx, token_idx + 1))
                        is_exclude.add(token_idx)

    if is_include_structure:
        for match in drug_matches:
            match_data = match[0]
            if "drugbank_id" in match_data:
                structure = dbid_to_mol_lookup.get(match_data["drugbank_id"])
                if structure is not None:
                    match_data["structure_mol"] = structure

    return drug_matches


reset_drugs_data()
