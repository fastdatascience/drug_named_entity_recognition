"""

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

"""

import re
from typing import Dict, Optional, Tuple, Union

import requests

# * IUPAC 2023 atomic weights for all elements
ATOMIC_WEIGHTS = {
    "H": 1.00794,
    "He": 4.002602,
    "Li": 6.941,
    "Be": 9.012182,
    "B": 10.811,
    "C": 12.0107,
    "N": 14.0067,
    "O": 15.9994,
    "F": 18.9984032,
    "Ne": 20.1797,
    "Na": 22.98976928,
    "Mg": 24.3050,
    "Al": 26.9815386,
    "Si": 28.0855,
    "P": 30.973762,
    "S": 32.065,
    "Cl": 35.453,
    "Ar": 39.948,
    "K": 39.0983,
    "Ca": 40.078,
    "Sc": 44.955912,
    "Ti": 47.867,
    "V": 50.9415,
    "Cr": 51.9961,
    "Mn": 54.938045,
    "Fe": 55.845,
    "Co": 58.933195,
    "Ni": 58.6934,
    "Cu": 63.546,
    "Zn": 65.38,
    "Ga": 69.723,
    "Ge": 72.64,
    "As": 74.92160,
    "Se": 78.96,
    "Br": 79.904,
    "Kr": 83.798,
    "Rb": 85.4678,
    "Sr": 87.62,
    "Y": 88.90585,
    "Zr": 91.224,
    "Nb": 92.90638,
    "Mo": 95.96,
    "Tc": 98.0,
    "Ru": 101.07,
    "Rh": 102.90550,
    "Pd": 106.42,
    "Ag": 107.8682,
    "Cd": 112.411,
    "In": 114.818,
    "Sn": 118.710,
    "Sb": 121.760,
    "Te": 127.60,
    "I": 126.90447,
    "Xe": 131.293,
    "Cs": 132.9054519,
    "Ba": 137.327,
    "La": 138.90547,
    "Ce": 140.116,
    "Pr": 140.90765,
    "Nd": 144.24,
    "Pm": 145.0,
    "Sm": 150.36,
    "Eu": 151.964,
    "Gd": 157.25,
    "Tb": 158.92534,
    "Dy": 162.500,
    "Ho": 164.93032,
    "Er": 167.259,
    "Tm": 168.93421,
    "Yb": 173.04,
    "Lu": 174.967,
    "Hf": 178.49,
    "Ta": 180.9479,
    "W": 183.84,
    "Re": 186.207,
    "Os": 190.23,
    "Ir": 192.217,
    "Pt": 195.084,
    "Au": 196.966569,
    "Hg": 200.59,
    "Tl": 204.3833,
    "Pb": 207.2,
    "Bi": 208.98040,
    "Po": 209.0,
    "At": 210.0,
    "Rn": 222.0,
    "Fr": 223.0,
    "Ra": 226.0,
    "Ac": 227.0,
    "Th": 232.03806,
    "Pa": 231.03588,
    "U": 238.02891,
    "Np": 237.0,
    "Pu": 244.0,
    "Am": 243.0,
    "Cm": 247.0,
    "Bk": 247.0,
    "Cf": 251.0,
    "Es": 252.0,
    "Fm": 257.0,
    "Md": 258.0,
    "No": 259.0,
    "Lr": 262.0,
    "Rf": 267.0,
    "Db": 270.0,
    "Sg": 271.0,
    "Bh": 270.0,
    "Hs": 277.0,
    "Mt": 278.0,
    "Ds": 281.0,
    "Rg": 282.0,
    "Cn": 285.0,
    "Fl": 289.0,
    "Lv": 293.0,
    "Ts": 294.0,
    "Og": 294.0,
}


def fetch_pub_chem_properties(
    drug_name: str,
) -> Union[Tuple[Optional[float], Optional[str]], Tuple[None, None]]:
    """
    Fetches MolecularWeight and CanonicalSMILES from PubChem API for a given drug name.

    Returns:
        MolecularWeight as float and CanonicalSMILES as strings if found, otherwise (None, None).
    """
    url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{drug_name}/property/MolecularWeight,CanonicalSMILES/JSON"
    try:
        response = requests.get(url, timeout=10)
        if response.ok:
            props = response.json()["PropertyTable"]["Properties"][0]
            # * Return as strings to preserve exact formatting from API
            return props.get("MolecularWeight"), props.get("CanonicalSMILES")
    except Exception:
        pass
    return None, None


def calculate_molecular_weight(formula: str) -> float:
    """
    Calculates the average molecular weight from a chemical formula string.
    Returns the molecular weight rounded to two decimals.
    """
    matches = re.findall(r"([A-Z][a-z]?)(\d*)", formula)
    weight = 0.0
    for element, count in matches:
        if element not in ATOMIC_WEIGHTS:
            raise ValueError(f"Unknown element: {element}")
        count = int(count) if count else 1
        weight += ATOMIC_WEIGHTS[element] * count
    return round(weight, 2)


def get_molecular_weight(match_data: dict, lookup_name: str) -> Dict:
    """
    Ensures 'molecular_weight' and 'smiles' are present in match_data.
    Tries to calculate molecular_weight from formula first; falls back to PubChem API if needed.
    Modifies match_data in place.
    """
    # * Try formula-based calculation first
    if "molecular_weight" not in match_data and "formula" in match_data:
        try:
            match_data["molecular_weight"] = calculate_molecular_weight(
                match_data["formula"]
            )
        except Exception:
            # * If formula is invalid or missing elements, fallback to API
            pass

    # * Fetch from PubChem if still missing molecular_weight
    if "molecular_weight" not in match_data:
        mw, _ = fetch_pub_chem_properties(lookup_name)
        if mw:
            match_data["molecular_weight"] = round(mw, 2)

    return match_data
