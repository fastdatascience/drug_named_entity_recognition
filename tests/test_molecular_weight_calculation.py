import unittest
from drug_named_entity_recognition.molecular_properties import (
    calculate_molecular_weight,
)


class TestMolecularWeightCalculation(unittest.TestCase):
    def test_molecular_weight_from_formula(self):
        test_cases = [
            ("C8H9NO2", 151.16),
            ("C187H291N45O59", None),
            ("C20H25N3O", 323.43),
        ]
        for formula, expected_weight in test_cases:
            weight = calculate_molecular_weight(formula)
            print("\n================ Molecular Weight Calculation ================")
            print(f"Testing formula: {formula}")
            print(f"Calculated molecular weight: {weight}")
            print("===============================================")

            if expected_weight is not None:
                print(f"Expected molecular weight: {expected_weight}")
                self.assertAlmostEqual(weight, expected_weight, places=2)
            else:
                print("No expected weight provided, just checking weight > 0")
                self.assertTrue(weight > 0)


if __name__ == "__main__":
    unittest.main()
