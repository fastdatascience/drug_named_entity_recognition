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

from drug_named_entity_recognition.drugs_finder import find_drugs, add_custom_drug_synonym, reset_drugs_data, \
    add_custom_new_drug, remove_drug_synonym


class TestDrugsFinderModifications(unittest.TestCase):

    def test_drug_synonym_not_working_first(self):
        reset_drugs_data()
        drugs = find_drugs("i bought some potato".split(" "))

        print(drugs)

        self.assertEqual(0, len(drugs))

    def test_drug_synonym_1(self):
        reset_drugs_data()
        add_custom_drug_synonym("potato", "sertraline")

        drugs = find_drugs("i bought some potato".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Sertraline", drugs[0][0]['name'])

    def test_completely_new_drug(self):
        reset_drugs_data()
        add_custom_new_drug("potato", {"name": "solanum tuberosum"})

        drugs = find_drugs("i bought some potato".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("solanum tuberosum", drugs[0][0]['name'])

    def test_drug_synonym_working_control(self):
        reset_drugs_data()
        drugs = find_drugs("i bought some Sertraline".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Sertraline", drugs[0][0]['name'])

    def test_drug_synonym_absent_after_erasure(self):
        reset_drugs_data()
        remove_drug_synonym("sertraline")

        drugs = find_drugs("i bought some Sertraline".split(" "))

        self.assertEqual(0, len(drugs))


if __name__ == "__main__":
    unittest.main()
