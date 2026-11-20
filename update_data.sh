#!/bin/bash

# Update script for Drug Named Entity Recognition library
# Downloads vocabularies and updates version numbers

set -e  # Exit on error

echo "=== Updating Drug Named Entity Recognition vocabularies ==="

# Step 1: Download and process MeSH data
echo ""
echo "Step 1: Downloading and processingMeSH dump..."
cd harvesting_data_from_source
python download_mesh_dump_and_extract_drug_names_and_synonyms.py

# Step 2: Download DrugBank vocabulary
echo ""
echo "Step 2: Downloading DrugBank vocabulary..."

echo "Fetching DrugBank releases page..."
DRUGBANK_PAGE=$(curl -s "https://go.drugbank.com/releases/latest#open-data")

# Extract the vocabulary URL using sed (more portable)
# e.g., https://go.drugbank.com/releases/5-1-13/downloads/all-drugbank-vocabulary
DRUGBANK_URL=$(echo "$DRUGBANK_PAGE" | sed -n 's/.*\(https:\/\/go\.drugbank\.com\/releases\/[a-z0-9-]*\/downloads\/all-drugbank-vocabulary\).*/\1/p' | head -1)

if [ -z "$DRUGBANK_URL" ]; then
    echo "Error: Could not find DrugBank vocabulary URL"
    exit 1
fi

TMPFILE="/tmp/tmp.zip"
echo "Downloading DrugBank dump from $DRUGBANK_URL to $TMPFILE..."
curl -L -o "$TMPFILE" "$DRUGBANK_URL" || {
    echo "Error: Failed to download DrugBank dump"
    exit 1
}

echo "Unzipping DrugBank dump..."
unzip -o "$TMPFILE" -d . || {
    echo "Error: Failed to unzip DrugBank dump"
    exit 1
}

rm -f "$TMPFILE"

# Step 3: Download SMILES from PubChem
echo ""
echo "Step 3: Downloading SMILES data from PubChem..."
python download_smiles_from_pubchem.py

# Step 4: Create dictionaries for SMILES and mass
echo ""
echo "Step 4: Creating SMILES and mass dictionaries..."
python make_dict_lc_mesh_name_to_smiles_and_mass.py

# Step 5: Combine all data sources
echo ""
echo "Step 5: Combining all data sources..."
python combine_data_sources.py

# Copy generated files to src directory
echo ""
echo "Copying generated files to src directory..."
cp -f "drugbank vocabulary.csv" "../src/drug_named_entity_recognition/"
cp -f "drugs_dictionary_mesh.csv" "../src/drug_named_entity_recognition/"

echo "Drug database updated successfully. To create a new release, run update_versions.sh"