# Harmony Python library

<!-- badges: start -->
![my badge](https://badgen.net/badge/Status/In%20Development/orange)

[![PyPI package](https://img.shields.io/badge/pip%20install-drug-named-entity-recognition-brightgreen)](https://pypi.org/project/drug-named-entity-recognition/) [![version number](https://img.shields.io/pypi/v/drug-named-entity-recognition?color=green&label=version)](https://github.com/fastdatascience/drug_named_entity_recognition/releases) [![License](https://img.shields.io/github/license/fastdatascience/drug_named_entity_recognition)](https://github.com/fastdatascience/drug_named_entity_recognition/blob/main/LICENSE)

<!-- badges: end -->

# Drug named entity recognition

Developed by Fast Data Science, https://fastdatascience.com

Source code at https://github.com/fastdatascience/drug_named_entity_recognition

Tutorial at https://fastdatascience.com/drug-named-entity-recognition-python-library/

This is a lightweight Python library for finding drug names in a string.

Please note this library finds only high confidence drugs.

It also only finds the English names of these drugs. Names in other languages are not supported.

It also doesn't find short code names of drugs, such as abbreviations commonly used in medicine, such as "Ceph" for "Cephradin" - as these are highly ambiguous.

# Requirements

Python 3.9 and above

## Who to contact?

You can contact Thomas Wood or Fast Data Science team at https://fastdatascience.com/.

# Installing drug named entity recognition Python package

You can install from [PyPI](https://pypi.org/project/drug-named-entity-recognition).

```
pip install drug-named-entity-recognition
```


# Usage examples

You must first tokenise your input text using a tokeniser of your choice (NLTK, spaCy, etc).

You pass a list of strings to the `find_drugs` function.

Example 1

```
from drug_named_entity_recognition import find_drugs

find_drugs("i bought some Phenoxymethylpenicillin".split(" "))
```

outputs a list of tuples.

```
[({'name': 'Phenoxymethylpenicillin',
   'synonyms': {'Penicillin', 'Phenoxymethylpenicillin'},
   'nhs_url': 'https://www.nhs.uk/medicines/phenoxymethylpenicillin',
   'drugbank_id': 'DB00417'},
  3,
  3)]
```

You can ignore case with:

```
find_drugs("i bought some phenoxymethylpenicillin".split(" "), is_ignore_case=True)
```

# Data sources

The main data source is from Drugbank, augmented by datasets from the NHS, MeSH, Medline Plus and Wikipedia.

## Update the Drugbank dictionary

If you want to update the dictionary, you can use the data dump from Drugbank and replace the file `drugbank vocabulary.csv`:

* Download the open data dump from https://go.drugbank.com/releases/latest#open-data

## Update the Wikipedia dictionary

If you want to update the Wikipedia dictionary, download the dump from:

* https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia

and run `extract_drug_names_and_synonyms_from_wikipedia_dump.py`

## Update the MeSH dictionary

If you want to update the dictionary, download the open data dump from https://www.nlm.nih.gov/ 

and run `extract_drug_names_and_synonyms_from_mesh_dump.py`


# License information

* Data from Drugbank is licensed under [CC0](https://go.drugbank.com/releases/latest#open-data).

```
To the extent possible under law, the person who associated CC0 with the DrugBank Open Data has waived all copyright and related or neighboring rights to the DrugBank Open Data. This work is published from: Canada.
```

* Text from Wikipedia data dump is licensed under [GNU Free Documentation License](https://www.gnu.org/licenses/fdl-1.3.html) and [Creative Commons Attribution-Share-Alike 3.0 License](https://creativecommons.org/licenses/by-sa/3.0/). [More information](https://dumps.wikimedia.org/legal.html).

## Contributing to the Drug Named Entity Recognition library

If you'd like to contribute to this project, you can contact us at https://fastdatascience.com/ or make a pull request on our [Github repository](https://github.com/fastdatascience/drug_named_entity_recognition). You can also [raise an issue](https://github.com/fastdatascience/drug_named_entity_recognition/issues). 

## Developing the Drug Named Entity Recognition library

### Automated tests

Test code is in **tests/** folder using [unittest](https://docs.python.org/3/library/unittest.html).

The testing tool `tox` is used in the automation with GitHub Actions CI/CD.

### Use tox locally

Install tox and run it:

```
pip install tox
tox
```

In our configuration, tox runs a check of source distribution using [check-manifest](https://pypi.org/project/check-manifest/) (which requires your repo to be git-initialized (`git init`) and added (`git add .`) at least), setuptools's check, and unit tests using pytest. You don't need to install check-manifest and pytest though, tox will install them in a separate environment.

The automated tests are run against several Python versions, but on your machine, you might be using only one version of Python, if that is Python 3.9, then run:

```
tox -e py39
```

Thanks to GitHub Actions' automated process, you don't need to generate distribution files locally. But if you insist, click to read the "Generate distribution files" section.

### Continuous integration/deployment to PyPI

This package is based on the template https://pypi.org/project/example-pypi-package/

This package

- uses GitHub Actions for both testing and publishing
- is tested when pushing `master` or `main` branch, and is published when create a release
- includes test files in the source distribution
- uses **setup.cfg** for [version single-sourcing](https://packaging.python.org/guides/single-sourcing-package-version/) (setuptools 46.4.0+)

## Re-releasing the package manually

The code to re-release Harmony on PyPI is as follows:

```
source activate py311
pip install twine
rm -rf dist
python setup.py sdist
twine upload dist/*
```

## Who worked on the Drug Named Entity Recognition library?

The tool was developed:

* Thomas Wood ([Fast Data Science](https://fastdatascience.com))

## License

MIT License. Copyright (c) 2023 [Fast Data Science](https://fastdatascience.com)


## Citing the Drug Named Entity Recognition library

Wood, T.A., Drug Named Entity Recognition [Computer software], Version 0.1, accessed at https://fastdatascience.com/drug-named-entity-recognition-python-library/, Fast Data Science Ltd (2022)

```
@unpublished{countrynamedentityrecognition,
    AUTHOR = {Wood, T.A.},
    TITLE  = {Drug Named Entity Recognition (Computer software), Version 0.1},
    YEAR   = {2022},
    Note   = {To appear},
}
```
