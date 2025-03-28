# Cross check the Drug Named Entity Recognition drugs against common English words

# You need to install NLTK to run this

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

import sys

sys.path.append("src")

from drug_named_entity_recognition.drugs_finder import drug_variant_to_canonical
from drug_named_entity_recognition.omop_api import get_omop_id_from_drug  # 🔥 OMOP API

print("Finding all drugs that are short")
print(f"Loaded {len(drug_variant_to_canonical)} drugs from drug_variant_to_canonical")


short_drug_names = set()
drugs_with_omop = []

for word in drug_variant_to_canonical:
    canonical_name = drug_variant_to_canonical[word]
    
    # Add short drugs to separate list
    if len(word) <= 3:
        short_drug_names.add(word.upper())

    # Get OMOP ID via API
    if isinstance(canonical_name, list):
        canonical_name = canonical_name[0]
    omop_id = get_omop_id_from_drug(canonical_name)

    
    # Store results
    drugs_with_omop.append({
        "variant": word,
        "canonical_name": canonical_name,
        "omop_id": omop_id
    })

# Output short drug names
print("\nShort drug names (length <= 3):")
print(list(short_drug_names))

# Output top 10 drugs with OMOP IDs
print("\nSample drugs with OMOP ID:")
for entry in drugs_with_omop[:10]:
    print(f"{entry['canonical_name']} (variant: {entry['variant']}) → OMOP ID: {entry['omop_id']}")
