import json
from drug_named_entity_recognition.drugs_finder import find_drugs

# Input text
input_text = "I bought some paracetamol yesterday"
tokens = input_text.lower().split()

print(f"Input Tokens: {tokens}")

# Call the drug recogniser (with OMOP enabled)
results = find_drugs(tokens, use_omop_api=True)

print(f"Raw Results: {results}")

# Build nicely formatted output
output = []
for result in results:
    data, start_idx, end_idx = result
    formatted = {
        "matched_text": input_text.split()[start_idx:end_idx + 1],
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

print("\nFormatted Output:\n")
print(json.dumps(output, indent=2))
