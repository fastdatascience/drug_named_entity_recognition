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

# This is a script where we clean up the drug dictionary by identifying if any of the exclusion words should really be included as drugs.

import os
import re
import sys
import time
import traceback
from tqdm import tqdm
import requests

MODEL = 'gpt-4o'

with open("words_to_check_with_ai.txt", "r", encoding="utf-8") as f:
    words_to_check_with_ai = f.read().split("\n")


headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + os.environ["OPENAI_API_KEY"],
}

bot_responses = [""] * len(words_to_check_with_ai)

for idx in tqdm(range(len(words_to_check_with_ai))):
    q = words_to_check_with_ai[idx]
    print(f"Asking question: {idx+1}: {q}")

    starttime = time.time()

    json_data = {
        'model': MODEL,
        'messages': [
            {"role": "user", "content": f"What is {q}?\n"},
        ],
    }
    for attempt in range(3):
        print("attempt calling GPT API:", attempt)
        try:
            response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=json_data)
            r = response.json()["choices"][0]["message"]["content"]
            break
        except:
            print("Try again")
            traceback.print_exc()
            time.sleep(10)
    bot_responses[idx] = re.sub(r'\s+', ' ', r)

    with open("ai_responses.txt", "w", encoding="utf-8") as f:
        for j in range(idx):
            f.write(words_to_check_with_ai[j] + "\t" + bot_responses[j] + "\n")

    endtime = time.time()

    print("\tReceived response: ", r)

