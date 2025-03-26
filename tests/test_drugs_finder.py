'''
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

'''

import unittest

from drug_named_entity_recognition.drugs_finder import find_drugs


class TestDrugsFinder(unittest.TestCase):

    def test_drugs_1(self):
        drugs = find_drugs("i bought some Sertraline".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Sertraline", drugs[0][0]['name'])

    #
    # def test_drugs_lowercase(self):
    #     drugs = find_drugs("i bought some sertraline".split(" "), is_ignore_case=False)
    #
    #     self.assertEqual(0, len(drugs))

    def test_drugs_synonym(self):
        drugs = find_drugs("i bought some Zoloft".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Sertraline", drugs[0][0]['name'])

    # def test_drugs_synonym_lc(self):
    #     drugs = find_drugs("i bought some zoloft".split(" "), is_ignore_case=False)
    #
    #     self.assertEqual(0, len(drugs))

    def test_generic_lc(self):
        drugs = find_drugs("i bought some Rimonabant".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Rimonabant", drugs[0][0]['name'])

    def test_two_word_drug(self):
        drugs = find_drugs("i bought some Amphotericin B".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Amphotericin B", drugs[0][0]['name'])

    def test_hemlibra(self):
        drugs = find_drugs("i bought some HEMLIBRA".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Emicizumab", drugs[0][0]['name'])

    def test_paracetamol(self):
        drugs = find_drugs("i bought some paracetamol".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Acetaminophen", drugs[0][0]['name'])
        # self.assertEqual("Acetaminophen", drugs[0][0]['generic_names'][0])

    def test_tylenol(self):
        drugs = find_drugs("i bought some tylenol".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Acetaminophen", drugs[0][0]['name'])
        # self.assertEqual("Acetaminophen", drugs[0][0]['generic_names'][0])

    def test_actemra(self):
        drugs = find_drugs("i bought some Actemra".split(" "))

        print(drugs[0])

        self.assertEqual(1, len(drugs))
        self.assertEqual("Tocilizumab", drugs[0][0]['name'])
        # self.assertEqual("Tocilizumab", drugs[0][0]['generic_names'][0])

    def test_insulin(self):
        drugs = find_drugs("i bought some insulin".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Insulin", drugs[0][0]['name'])

    def test_acetylsalicylic_acid(self):
        drugs = find_drugs("i bought some acetylsalicylic acid".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Aspirin", drugs[0][0]['name'])

    #
    # def test_acetylsalicylic_acid_case_sensitive(self):
    #     drugs = find_drugs("i bought some acetylsalicylic acid".split(" "), is_ignore_case=False)
    #
    #     self.assertEqual(1, len(drugs))
    #     self.assertEqual("Aspirin", drugs[0][0]['name'])

    def test_polysporin(self):
        drugs = find_drugs("i bought some Polysporin".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Bacitracin/polymyxin B", drugs[0][0]['name'])

    def test_glycyrrhiza(self):
        drugs = find_drugs("i bought some Glycyrrhiza Spp. Root".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Glycyrrhiza glabra", drugs[0][0]['name'])

    def test_structure(self):
        drugs = find_drugs("i bought some Bivalirudin".split(" "), is_include_structure=True)

        self.assertEqual(1, len(drugs))
        self.assertEqual("Bivalirudin", drugs[0][0]['name'])
        self.assertIn("0.0000 C", drugs[0][0]['structure_mol'])

    def test_structure_2(self):
        drugs = find_drugs("i bought some Guaifenesin".split(" "), is_include_structure=True)

        self.assertEqual(1, len(drugs))
        self.assertEqual("Guaifenesin", drugs[0][0]['name'])
        self.assertIn("0.0000 C", drugs[0][0]['structure_mol'])

    def test_penicillin_streptomycin(self):
        drugs = find_drugs("i bought some Penicillin streptomycin".split(" "), is_include_structure=True)

        self.assertEqual(2, len(drugs))  # should be 1?

    def test_mounjaro(self):
        drugs = find_drugs("i bought some Mounjaro".split(" "), is_include_structure=True)

        self.assertEqual(1, len(drugs))

    def test_dry_ice(self):
        drugs = find_drugs("i bought some dry ice".split(" "), is_include_structure=True)

        self.assertEqual(0, len(drugs))

    def test_mounjaro_misspelt(self):
        drugs = find_drugs("i bought some Monjaro".split(" "), is_include_structure=True, is_fuzzy_match=True)

        import json
        print(json.dumps(drugs, indent=4))

        self.assertEqual(1, len(drugs))

    def test_restasis(self):
        drugs = find_drugs("i bought some restasis".split(" "), is_include_structure=True)

        self.assertEqual(1, len(drugs))


if __name__ == "__main__":
    unittest.main()
