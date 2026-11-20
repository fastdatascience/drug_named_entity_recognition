#!/bin/bash

# Update version numbers script for Drug Named Entity Recognition library
# Increments patch version and updates all version references

set -e  # Exit on error

# Step 3: Update version numbers
echo ""
echo "Step 3: Updating version numbers..."

# Read current version from __init__.py
INIT_FILE="src/drug_named_entity_recognition/__init__.py"
OLD_VERSION=$(grep '__version__' "$INIT_FILE" | awk -F'"' '{print $2}')

if [ -z "$OLD_VERSION" ]; then
    echo "Error: Could not find version in $INIT_FILE"
    exit 1
fi

echo "Current version: $OLD_VERSION"

# Increment patch version (last number)
VERSION_BITS=($(echo "$OLD_VERSION" | tr '.' ' '))
PATCH_VERSION=$((VERSION_BITS[2] + 1))
NEW_VERSION="${VERSION_BITS[0]}.${VERSION_BITS[1]}.${PATCH_VERSION}"

echo "New version: $NEW_VERSION"

# Update __init__.py
awk -v old="$OLD_VERSION" -v new="$NEW_VERSION" \
    '{gsub("\"" old "\"", "\"" new "\""); print}' \
    "$INIT_FILE" > "$INIT_FILE.tmp" && mv "$INIT_FILE.tmp" "$INIT_FILE"

# Update CITATION.cff
CITATION_FILE="CITATION.cff"
awk -v old="$OLD_VERSION" -v new="$NEW_VERSION" \
    '/^version:/ {gsub(old, new); print; next} {print}' \
    "$CITATION_FILE" > "$CITATION_FILE.tmp" && mv "$CITATION_FILE.tmp" "$CITATION_FILE"

# Update pyproject.toml
PYPROJECT_FILE="pyproject.toml"
awk -v old="$OLD_VERSION" -v new="$NEW_VERSION" \
    '/^version/ {gsub("\"" old "\"", "\"" new "\""); print; next} {print}' \
    "$PYPROJECT_FILE" > "$PYPROJECT_FILE.tmp" && mv "$PYPROJECT_FILE.tmp" "$PYPROJECT_FILE"

# Update README.md
README_FILE="README.md"
awk -v old="$OLD_VERSION" -v new="$NEW_VERSION" \
    '/Version / {gsub("Version " old, "Version " new); print; next} {print}' \
    "$README_FILE" > "$README_FILE.tmp" && mv "$README_FILE.tmp" "$README_FILE"

# Step 4: Git operations
echo ""
echo "Step 4: Staging files for git..."
git add "$INIT_FILE"
git add "$CITATION_FILE" "$README_FILE"
git add "src/drug_named_entity_recognition/drugbank vocabulary.csv"
git add "src/drug_named_entity_recognition/drugs_dictionary_mesh.csv"

echo ""
echo "Step 5: Committing changes..."
git commit -m "Update Drugbank and MeSH"

echo ""
echo "Step 6: Pushing to remote..."
git push

echo ""
echo "=== Update complete! ==="
echo "Version updated from $OLD_VERSION to $NEW_VERSION"
echo ""
echo "To create a GitHub release, run:"
echo "  gh release create \"v${NEW_VERSION}\""

