import json
import os
import traceback
import time
import requests

all_nhs_drugs = []
access_token = os.getenv("NHS_API_ACCESS_TOKEN")
# You can get API sandbox credentials from: https://onboarding.prod.api.platform.nhs.uk/MyApplications/ApplicationDetails/EditAPIKeys?appId=27d2bbf8-76a3-4788-8302-bc8740da9491
endpoint_url = 'https://int.api.service.nhs.uk/nhs-website-content/medicines'
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
    'apikey': access_token
}

already_seen = set()

for page_no in range(1, 20):

    print("page", page_no)

    try:

        params = {
            'page': str(page_no)
        }

        response = requests.get(endpoint_url, headers=headers, params=params)

        response_json = response.json()

        if 'significantLink' not in response_json:
            print("No 'significantLink' found in JSON. Exiting...")
            break

        print("number of responses:", len(response_json['significantLink']))

        if len(response_json['significantLink']) == 0:
            break

        first_item_url = response_json['significantLink'][0]['url']

        if first_item_url in already_seen:
            break

        for link in response_json['significantLink']:
            item_url = link['url']
            already_seen.add(item_url)

        print(f"Name of first drug returned by API on page {page_no}:", response_json['significantLink'][0]['name'])

        all_nhs_drugs.extend(response_json['significantLink'])

    except:
        print("Exiting loop.", traceback.format_exc())
        break

    time.sleep(30)

with open("all_nhs_drugs.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(all_nhs_drugs, indent=4))
