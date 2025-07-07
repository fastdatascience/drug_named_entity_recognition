import unittest
from unittest.mock import patch
from drug_named_entity_recognition.drugs_finder import find_drugs


class TestFindDrugsPubchemEnrichment(unittest.TestCase):
    @patch("drug_named_entity_recognition.molecular_properties.fetch_pub_chem_properties")
    def test_find_drugs_pub_chem_enrichment(self, mock_fetch):
        mock_molecular_weight = 151.16
        mock_smiles = "CC(=O)NC1=CC=C(C=C1)O"
        mock_fetch.return_value = (mock_molecular_weight, mock_smiles)

        tokens = ["paracetamol"]
        results = find_drugs(tokens)
        self.assertGreater(len(results), 0, "No matches found for 'paracetamol'")
        match_data = results[0][0]

        print("\n================ Molecular Weight ================")
        print("Molecular weight:", match_data["molecular_weight"])
        print("Smiles:", match_data["smiles"])
        print("===============================================")

        self.assertIn("molecular_weight", match_data)
        self.assertEqual(match_data["molecular_weight"], mock_molecular_weight)
        self.assertIn("smiles", match_data)
        self.assertEqual(match_data["smiles"], mock_smiles)


if __name__ == "__main__":
    unittest.main()
