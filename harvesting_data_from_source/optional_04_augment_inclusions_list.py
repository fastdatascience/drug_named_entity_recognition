import json
import re

import pandas as pd

from inclusions import common_english_words_to_include_in_drugs_dictionary

df = pd.read_csv("ai_responses.txt", sep="\t", encoding="utf-8", names=["word", "ai_response"])

new_inclusion_words = set()

for idx in range(len(df)):
    x = df.ai_response.iloc[idx].lower()
    if "drug" in x or "medicinal" in x or "traditional medicine" in x or "herbal medicine" in x or "chinese medicine" in x or "pharmacological" in x or "medication" in x:
        word = df.word.iloc[idx]
        new_inclusion_words.add(word)

print("New inclusion words:")

print(json.dumps(list(new_inclusion_words), indent=4))

all_inclusion_words = sorted(common_english_words_to_include_in_drugs_dictionary.union(new_inclusion_words))

TEMPLATE = """'''
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

common_english_words_to_include_in_drugs_dictionary = """

serialised = json.dumps(all_inclusion_words, indent=4)
serialised = re.sub(r'\[', "{", serialised)
serialised = re.sub(r'\]', "}", serialised)

with open("new_inclusions.py", "w", encoding="utf-8") as f:
    f.write(TEMPLATE + serialised)
