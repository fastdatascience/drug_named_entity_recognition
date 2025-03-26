import requests

def get_rxcui(drug_name):
    try:
        url = f"https://rxnav.nlm.nih.gov/REST/rxcui.json?name={drug_name}"
        response = requests.get(url)
        rxnorm_ids = response.json().get("idGroup", {}).get("rxnormId")
        return rxnorm_ids[0] if rxnorm_ids else None
    except Exception as e:
        print(f"Error fetching RxCUI for {drug_name}: {e}")
        return None

def get_omop_properties(rxcui):
    try:
        url = f"https://rxnav.nlm.nih.gov/REST/rxcui/{rxcui}/allProperties.json?prop=all"
        response = requests.get(url)
        return response.json()
    except Exception as e:
        print(f"Error fetching OMOP properties for RxCUI {rxcui}: {e}")
        return None

def extract_omop_id(properties_json):
    try:
        prop_concepts = properties_json.get("propConceptGroup", {}).get("propConcept", [])
        for item in prop_concepts:
            if item.get("propCategory") == "ATC":  # Closest available to OMOP vocab
                return item.get("propName")
        return None
    except Exception as e:
        print(f"Error extracting OMOP ID: {e}")
        return None

def get_omop_id_from_drug(drug_name):
    rxcui = get_rxcui(drug_name)
    if not rxcui:
        return None
    properties = get_omop_properties(rxcui)
    return extract_omop_id(properties)
