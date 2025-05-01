from rdkit import Chem
from rdkit.Chem import Draw
from drug_named_entity_recognition import find_drugs
sentences = "I prescribed semaglutide"
drugs = find_drugs(sentences.split())
for drug in drugs:
    smiles = drug[0]["smiles"]
    break
print (smiles)

mol = Chem.MolFromSmiles(smiles)
image = Draw.MolToImage(mol)
image.show()
