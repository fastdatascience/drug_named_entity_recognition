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

from drug_named_entity_recognition.drugs_finder import find_drugs, reset_drugs_data


class TestFormula(unittest.TestCase):

    def test_paracetamol_has_formula(self):
        tokens = ["paracetamol"]
        matches = find_drugs(tokens)

        self.assertGreater(len(matches), 0, "No matches found for 'paracetamol'")
        match_data = matches[0][0]

        self.assertIn("formula", match_data, "formula field not found in match data")
        self.assertIsInstance(match_data["formula"], str, "formula is not a string")
        self.assertGreater(len(match_data["formula"]), 0, "formula string is empty")
        self.assertEqual("C8H9NO2", match_data["formula"])

        print("\n================ formula Output ================")
        print(match_data["formula"])
        print("===============================================")

    def test_ozempic_has_formula(self):
        tokens = ["ozempic"]
        matches = find_drugs(tokens)

        self.assertGreater(len(matches), 0, "No matches found for 'ozempic'")
        match_data = matches[0][0]

        self.assertIn("formula", match_data, "formula field not found in match data")
        self.assertIsInstance(match_data["formula"], str, "formula is not a string")
        self.assertGreater(len(match_data["formula"]), 0, "formula string is empty")
        self.assertEqual("C187H291N45O59", match_data["formula"])

        print("\n================ formula Output ================")
        print(match_data["formula"])
        print("===============================================")


if __name__ == "__main__":
    unittest.main()
