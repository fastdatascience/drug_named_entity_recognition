"""
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

"""

# This script downloads the SMILES data from Pubchem and unzips where necessary.
# Note that we have to get two files: one is Pubchem ID to SMILES, and one is Pubchem ID to MeSH name (not MeSH ID)
# We can later join these to get MeSH name to SMILES

import gzip
import os
import requests
import shutil

url_pubchem_mesh = "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-MeSH"
output_file_pubchem_mesh = "CID-MeSH"

# Download MeSH file
print(
    f"Downloading Pubchem MeSH dump for SMILES from {url_pubchem_mesh} to {output_file_pubchem_mesh}..."
)
response = requests.get(url_pubchem_mesh)
response.raise_for_status()

with open(output_file_pubchem_mesh, "wb") as f:
    f.write(response.content)

print(
    f"Downloaded Pubchem MeSH dump for SMILES from {url_pubchem_mesh} to {output_file_pubchem_mesh}."
)

# Download SMILES file
url_pubchem_smiles = (
    "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-SMILES.gz"
)
output_file_pubchem_smiles = "CID-SMILES.gz"

print(
    f"Downloading Pubchem SMILES data from {url_pubchem_smiles} to {output_file_pubchem_smiles}..."
)
response = requests.get(url_pubchem_smiles)
response.raise_for_status()

with open(output_file_pubchem_smiles, "wb") as f:
    f.write(response.content)

print(
    f"Downloaded Pubchem SMILES data from {url_pubchem_smiles} to {output_file_pubchem_smiles}."
)

# Download mass file
url_pubchem_mass = "https://ftp.ncbi.nlm.nih.gov/pubchem/Compound/Extras/CID-Mass.gz"
output_file_pubchem_mass = "CID-Mass.gz"

print(
    f"Downloading Pubchem mass data from {url_pubchem_mass} to {output_file_pubchem_mass}..."
)
response = requests.get(url_pubchem_mass)
response.raise_for_status()

with open(output_file_pubchem_mass, "wb") as f:
    f.write(response.content)

print(
    f"Downloaded Pubchem mass data from {url_pubchem_mass} to {output_file_pubchem_mass}."
)

# Unzip SMILES file
print(f"Unzipping {output_file_pubchem_smiles}...")
with gzip.open(output_file_pubchem_smiles, "rb") as f_in:
    with open(output_file_pubchem_smiles[:-3], "wb") as f_out:  # Remove .gz extension
        shutil.copyfileobj(f_in, f_out)

print(f"Unzipped {output_file_pubchem_smiles}.")

# Unzip mass file
print(f"Unzipping {output_file_pubchem_mass}...")
with gzip.open(output_file_pubchem_mass, "rb") as f_in:
    with open(output_file_pubchem_mass[:-3], "wb") as f_out:  # Remove .gz extension
        shutil.copyfileobj(f_in, f_out)

print(f"Unzipped {output_file_pubchem_mass}.")
