import json
import re

re_num = re.compile(r'^\d+$')
re_three_digits = re.compile(r'\d\d\d')

pubchem_id_to_name_lc = {}
with open("CID-MeSH", "r", encoding="utf-8") as f:
    for line in f:
        cols = line.strip().split("\t")
        pubchem_id_to_name_lc[cols[0]] = cols[1].strip().lower()

pubchem_id_to_smiles = {}
with open("CID-SMILES", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i % 500000 == 0:
            print(f"[INFO] Processed {i} SMILES lines...")
        cols = line.strip().split("\t")

        if cols[0] in pubchem_id_to_name_lc:
            pubchem_id_to_smiles[cols[0]] = cols[1]

pubchem_id_to_mass = {}
with open("CID-Mass", "r", encoding="utf-8") as f:
    for i, line in enumerate(f):
        if i % 500000 == 0:
            print(f"[INFO] Processed {i} Mass lines...")
        cols = line.strip().split("\t")

        if cols[0] in pubchem_id_to_name_lc:
            pubchem_id_to_mass[cols[0]] = cols[1:2] + [float(x) for x in cols[2:]]

mesh_name_to_smiles = {}
for pubchem_id, smiles in pubchem_id_to_smiles.items():
    name = pubchem_id_to_name_lc[pubchem_id]
    mesh_name_to_smiles[name] = smiles
mesh_name_to_mass = {}
for pubchem_id, mass_data in pubchem_id_to_mass.items():
    name = pubchem_id_to_name_lc[pubchem_id]
    mesh_name_to_mass[name] = mass_data

with open("mesh_name_to_smiles.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(mesh_name_to_smiles, indent=4))

with open("mesh_name_to_mass.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(mesh_name_to_mass, indent=4))
