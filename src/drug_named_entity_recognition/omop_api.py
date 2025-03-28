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

import requests

# Local cache
omop_cache = {}

def get_rxcui(drug_name):
    if drug_name in omop_cache:
        return omop_cache[drug_name]  

    try:
        url = f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}"
        response = requests.get(url)
        rxnorm_ids = response.json().get("idGroup", {}).get("rxnormId")
        omop_id = rxnorm_ids[0] if rxnorm_ids else None
        omop_cache[drug_name] = omop_id  
        return omop_id
    except Exception as e:
        print(f"Error fetching RxCUI for {drug_name}: {e}")
        return None

def get_omop_id_from_drug(drug_name):
    print(f"🔍 Looking up OMOP ID for: {drug_name}")
    rxcui = get_rxcui(drug_name)
    print(f"→ RxCUI (used as OMOP ID): {rxcui}")
    return rxcui
