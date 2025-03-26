import json
from drug_named_entity_recognition.drugs_finder import find_drugs

# Test input
input_text = "I bought some paracetamol yesterday"
tokens = input_text.lower().split()

# Call the drug recogniser
results = find_drugs(tokens)

# Build pretty output
output = []
for result in results:
    data, start_idx, end_idx = result
    formatted = {
        "input": input_text[start_idx:end_idx+1],
        "results": {
            "name": data.get("name", ""),
            "omop_id": data.get("omop_id", ""),
            "medline_plus_id": data.get("medline_plus_id", ""),
            "nhs_api_url": data.get("nhs_api_url", ""),
            "nhs_url": data.get("nhs_url", ""),
            "mesh_id": data.get("mesh_id", ""),
            "drugbank_id": data.get("drugbank_id", ""),
            "wikipedia_url": data.get("wikipedia_url", ""),
            "synonyms": data.get("synonyms", []),
            "match_type": data.get("match_type", ""),
            "matching_string": data.get("matching_string", "")
        }
    }
    output.append(formatted)

# Print JSON pretty
print(json.dumps(output, indent=2))
