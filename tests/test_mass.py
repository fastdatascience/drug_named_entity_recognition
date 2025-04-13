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


class TestMass(unittest.TestCase):

    def test_paracetamol_has_mass(self):
        tokens = ["paracetamol"]
        matches = find_drugs(tokens)

        self.assertGreater(len(matches), 0, "No matches found for 'paracetamol'")
        match_data = matches[0][0]

        self.assertIn("mass_lower", match_data, "mass field not found in match data")
        self.assertIsInstance(match_data["mass_lower"], float, "mass is not a float")
        self.assertGreater(match_data["mass_lower"], 151, )
        self.assertLess(match_data["mass_upper"], 152, )

        print("\n================ Mass Output ================")
        print("Lower bound mass:", match_data["mass_lower"])
        print("Upper bound mass:", match_data["mass_upper"])
        print("===============================================")

    def test_ozempic_has_mass(self):
        tokens = ["ozempic"]
        matches = find_drugs(tokens)

        self.assertGreater(len(matches), 0, "No matches found for 'ozempic'")
        match_data = matches[0][0]

        self.assertIn("mass_lower", match_data, "mass field not found in match data")
        self.assertIsInstance(match_data["mass_lower"], float, "mass is not a float")
        self.assertGreater(match_data["mass_lower"], 4111, )
        self.assertLess(match_data["mass_upper"], 4115, )

        print("\n================ Mass Output ================")
        print("Lower bound mass:", match_data["mass_lower"])
        print("Upper bound mass:", match_data["mass_upper"])
        print("===============================================")


if __name__ == "__main__":
    unittest.main()
