"""

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

"""

import bz2
import logging
import os
import pathlib
import pickle as pkl

try:
    from cfuzzyset import cFuzzySet as FuzzySet
except ImportError:
    from fuzzyset import FuzzySet

from english_words import get_english_words_set

from drug_named_entity_recognition.molecular_properties import (
    get_molecular_weight,
)
from drug_named_entity_recognition.omop_api import get_omop_id_from_drug
from drug_named_entity_recognition.structure_file_downloader import download_structures
from drug_named_entity_recognition.util import stopwords

logger = logging.getLogger(__name__)

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

# FuzzySet for drug names and English dictionary
drug_names_fuzzyset = None
dictionary_fuzzyset = None


def get_ngrams(text):
    n = 3
    ngrams = set()
    for i in range(0, len(text) - n + 1, 1):
        ngrams.add(text[i : i + n])
    return ngrams


def reset_drugs_data():
    global drug_names_fuzzyset, dictionary_fuzzyset

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

    # Build FuzzySet for drug names
    drug_names_fuzzyset = FuzzySet()
    for drug_variant in drug_variant_to_canonical:
        drug_names_fuzzyset.add(drug_variant.lower())
    logger.info("Built FuzzySet with %s drug variants", len(drug_variant_to_canonical))

    # Build FuzzySet for English dictionary
    dictionary_fuzzyset = FuzzySet()
    for term in get_english_words_set(["web2"], lower=True):
        dictionary_fuzzyset.add(term)
    logger.info("Built FuzzySet for English dictionary")


def add_custom_drug_synonym(
    drug_variant: str, canonical_name: str, optional_variant_data: dict = None
):
    global drug_names_fuzzyset

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

    # Add to FuzzySet if it exists
    if drug_names_fuzzyset is not None:
        drug_names_fuzzyset.add(drug_variant)

    return f"Added {drug_variant} as a synonym for {canonical_name}. Optional data attached to this synonym = {optional_variant_data}"


def add_custom_new_drug(drug_name, drug_data):
    drug_name = drug_name.lower()
    drug_canonical_to_data[drug_name] = drug_data
    add_custom_drug_synonym(drug_name, drug_name)

    return f"Added {drug_name} to the tool with data {drug_data}"


def remove_drug_synonym(drug_variant: str):
    global drug_names_fuzzyset

    drug_variant = drug_variant.lower()
    ngrams = get_ngrams(drug_variant)

    del variant_to_ngrams[drug_variant]
    del drug_variant_to_canonical[drug_variant]
    if drug_variant in drug_variant_to_variant_data:
        del drug_variant_to_variant_data[drug_variant]

    for ngram in ngrams:
        if ngram in ngram_to_variant:
            ngram_to_variant[ngram].remove(drug_variant)

    # Note: FuzzySet doesn't support removal, so we'd need to rebuild it
    # For now, we'll just note that removal won't affect FuzzySet until reset_drugs_data() is called
    # In practice, this is acceptable since removals are rare

    return f"Removed {drug_variant} from dictionary"


def get_fuzzy_match(surface_form: str, fuzzy_threshold: float = 0.5):
    """Find fuzzy match for surface form using FuzzySet, excluding common English words.

    Args:
        surface_form: The text to match against drug names
        fuzzy_threshold: Minimum similarity score (0-1) for a match (default: 0.5)

    Returns:
        Tuple of (matched_variant, similarity_score) or (None, None) if no match found
    """
    if drug_names_fuzzyset is None or dictionary_fuzzyset is None:
        logger.warning("FuzzySets not initialized. Call reset_drugs_data() first.")
        return None, None

    surface_form_lower = surface_form.lower()

    # Try to find in drug_names FuzzySet
    drug_results = drug_names_fuzzyset.get(surface_form_lower)
    if not drug_results:
        return None, None

    best_score, best_match = drug_results[0]

    # Check if score meets threshold
    if best_score < fuzzy_threshold:
        return None, None

    # Check if it's a common English word in the dictionary
    dict_results = dictionary_fuzzyset.get(surface_form_lower)
    is_dict_word = dict_results and dict_results[0][0] >= best_score

    # If it's a dictionary word with higher or equal score, exclude it
    if is_dict_word:
        return None, None

    # Return the matched variant and score
    return best_match, best_score


def find_drugs(
    tokens: list,
    is_fuzzy_match=False,
    is_ignore_case=None,
    is_include_structure=False,
    is_use_omop_api=False,
    use_pub_chem_api=False,
):
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
                match_data = dict(
                    drug_canonical_to_data.get(m, {})
                ) | drug_variant_to_variant_data.get(cand_norm, {})
                match_data["match_similarity"] = 1.0
                match_data["matching_string"] = cand
                lookup_name = match_data.get("name", m)

                match_data = get_molecular_weight(
                    match_data, lookup_name, use_pub_chem_api
                )

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
                        match_data = dict(
                            drug_canonical_to_data.get(m, {})
                        ) | drug_variant_to_variant_data.get(fuzzy_matched_variant, {})
                        match_data["match_similarity"] = similarity
                        match_data["match_variant"] = fuzzy_matched_variant
                        match_data["matching_string"] = cand
                        lookup_name = match_data.get("name", m)

                        match_data = get_molecular_weight(
                            match_data, lookup_name, use_pub_chem_api
                        )

                        if is_use_omop_api: 
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
                match_data = dict(
                    drug_canonical_to_data.get(m, {})
                ) | drug_variant_to_variant_data.get(cand_norm, {})
                match_data["match_similarity"] = 1.0
                match_data["matching_string"] = token
                lookup_name = match_data.get("name", m)

                match_data = get_molecular_weight(
                    match_data, lookup_name, use_pub_chem_api
                )

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
                        match_data = dict(
                            drug_canonical_to_data.get(m, {})
                        ) | drug_variant_to_variant_data.get(fuzzy_matched_variant, {})
                        match_data["match_similarity"] = similarity
                        match_data["match_variant"] = fuzzy_matched_variant
                        match_data["matching_string"] = token
                        lookup_name = match_data.get("name", m)

                        match_data = get_molecular_weight(
                            match_data, lookup_name, use_pub_chem_api
                        )

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
