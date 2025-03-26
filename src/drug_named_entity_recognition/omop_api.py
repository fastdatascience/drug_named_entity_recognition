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
