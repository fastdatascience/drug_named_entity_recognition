from rdkit import Chem
from rdkit.Chem import Draw
from drug_named_entity_recognition import find_drugs
sentences = "I prescribed semaglutide"
drugs = find_drugs(sentences.split(), is_include_structure=True)
for drug in drugs:
    structure_mol = drug[0]["structure_mol"]
    break
print (structure_mol)

mol = Chem.MolFromMolBlock(structure_mol)
image = Draw.MolToImage(mol)
image.show()
