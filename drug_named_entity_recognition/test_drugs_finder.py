import unittest

from drug_named_entity_recognition.drugs_finder import find_drugs

class TestDrugsFinder(unittest.TestCase):

    def test_drugs_1(self):
        drugs = find_drugs("i bought some Sertraline".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Sertraline", drugs[0][0]['name'])

    def test_drugs_lowercase(self):
        drugs = find_drugs("i bought some sertraline".split(" "))

        self.assertEqual(0, len(drugs))

    def test_drugs_synonym(self):
        drugs = find_drugs("i bought some Zoloft".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Sertraline", drugs[0][0]['name'])

    def test_drugs_synonym_lc(self):
        drugs = find_drugs("i bought some zoloft".split(" "))

        self.assertEqual(0, len(drugs))

    def test_generic_lc(self):
        drugs = find_drugs("i bought some penicillin".split(" "))

        self.assertEqual(2, len(drugs))
        self.assertEqual("Phenoxymethylpenicillin", drugs[0][0]['name'])

    def test_two_word_drug(self):
        drugs = find_drugs("i bought some Amphotericin B".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Amphotericin B", drugs[0][0]['name'])

    def test_hemlibra(self):
        drugs = find_drugs("i bought some HEMLIBRA".split(" "))

        self.assertEqual(1, len(drugs))
        self.assertEqual("Emicizumab", drugs[0][0]['name'])
