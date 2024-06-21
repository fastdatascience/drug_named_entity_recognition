![Fast Data Science logo](https://raw.githubusercontent.com/fastdatascience/brand/main/primary_logo.svg)

<a href="https://fastdatascience.com"><span align="left">🌐 fastdatascience.com</span></a>
<a href="https://www.linkedin.com/company/fastdatascience/"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/linkedin.svg" alt="Fast Data Science | LinkedIn" width="21px"/></a>
<a href="https://twitter.com/fastdatascienc1"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/x.svg" alt="Fast Data Science | X" width="21px"/></a>
<a href="https://www.instagram.com/fastdatascience/"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/instagram.svg" alt="Fast Data Science | Instagram" width="21px"/></a>
<a href="https://www.facebook.com/fastdatascienceltd"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/fb.svg" alt="Fast Data Science | Facebook" width="21px"/></a>
<a href="https://www.youtube.com/channel/UCLPrDH7SoRT55F6i50xMg5g"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/yt.svg" alt="Fast Data Science | YouTube" width="21px"/></a>
<a href="https://g.page/fast-data-science"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/google.svg" alt="Fast Data Science | Google" width="21px"/></a>
<a href="https://medium.com/fast-data-science"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/medium.svg" alt="Fast Data Science | Medium" width="21px"/></a>
<a href="https://mastodon.social/@fastdatascience"><img align="left" src="https://raw.githubusercontent.com//harmonydata/.github/main/profile/mastodon.svg" alt="Fast Data Science | Mastodon" width="21px"/></a>

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.10970631.svg)](https://doi.org/10.5281/zenodo.10970631)


You can run the walkthrough Python notebook in [Google Colab](https://colab.research.google.com/github/fastdatascience/drug_named_entity_recognition/blob/main/drug_named_entity_recognition_example_walkthrough.ipynb) with a single click: <a href="https://colab.research.google.com/github/fastdatascience/drug_named_entity_recognition/blob/main/drug_named_entity_recognition_example_walkthrough.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# Drug named entity recognition Python library by Fast Data Science

<!-- badges: start -->
![my badge](https://badgen.net/badge/Status/In%20Development/orange)
[![PyPI package](https://img.shields.io/badge/pip%20install-drug_named_entity_recognition-brightgreen)](https://pypi.org/project/drug-named-entity-recognition/) [![version number](https://img.shields.io/pypi/v/drug-named-entity-recognition?color=green&label=version)](https://github.com/fastdatascience/drug_named_entity_recognition/releases) [![License](https://img.shields.io/github/license/fastdatascience/drug_named_entity_recognition)](https://github.com/fastdatascience/drug_named_entity_recognition/blob/main/LICENSE)
[![pypi Version](https://img.shields.io/pypi/v/drug_named_entity_recognition.svg?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/drug_named_entity_recognition/)
 [![version number](https://img.shields.io/pypi/v/drug_named_entity_recognition?color=green&label=version)](https://github.com/fastdatascience/drug_named_entity_recognition/releases) [![PyPi downloads](https://static.pepy.tech/personalized-badge/drug_named_entity_recognition?period=total&units=international_system&left_color=grey&right_color=orange&left_text=pip%20downloads)](https://pypi.org/project/drug_named_entity_recognition/)
[![forks](https://img.shields.io/github/forks/fastdatascience/drug_named_entity_recognition)](https://github.com/fastdatascience/drug_named_entity_recognition/forks)

<!-- badges: end -->

# 💊 Drug named entity recognition

Developed by Fast Data Science, https://fastdatascience.com

Source code at https://github.com/fastdatascience/drug_named_entity_recognition

Tutorial at https://fastdatascience.com/drug-named-entity-recognition-python-library/

This is a lightweight Python library for finding drug names in a string, otherwise known as [named entity recognition (NER)](https://fastdatascience.com/named-entity-recognition/) and named entity linking.

Please note this library finds only high confidence drugs and doesn't support misspellings at present.

It also only finds the English names of these drugs. Names in other languages are not supported.

It also doesn't find short code names of drugs, such as abbreviations commonly used in medicine, such as "Ceph" for "Cephradin" - as these are highly ambiguous.

# 💻Installing drug named entity recognition Python package

You can install from [PyPI](https://pypi.org/project/drug-named-entity-recognition).

```
pip install drug-named-entity-recognition
```

If you get an error installing, try making a new Python environment in Conda (`conda create -n test-env; conda activate test-env`) or Venv (`python -m testenv; source testenv/bin/activate` / `testenv\Scripts\activate`) and then installing the library.

The library already contains the drug names so if you don't need to update the dictionary, then you should not have to run any of the download scripts.

If you have problems installing, try our [Google Colab](https://colab.research.google.com/github/fastdatascience/drug_named_entity_recognition/blob/main/drug_named_entity_recognition_example_walkthrough.ipynb) walkthrough.

# 💡Usage examples

You must first tokenise your input text using a tokeniser of your choice (NLTK, spaCy, etc).

You pass a list of strings to the `find_drugs` function.

Example 1

```
from drug_named_entity_recognition import find_drugs

find_drugs("i bought some Prednisone".split(" "))
```

outputs a list of tuples.

```
[({'name': 'Prednisone', 'synonyms': {'Sone', 'Sterapred', 'Deltasone', 'Panafcort', 'Prednidib', 'Cortan', 'Rectodelt', 'Prednisone', 'Cutason', 'Meticorten', 'Panasol', 'Enkortolon', 'Ultracorten', 'Decortin', 'Orasone', 'Winpred', 'Dehydrocortisone', 'Dacortin', 'Cortancyl', 'Encorton', 'Encortone', 'Decortisyl', 'Kortancyl', 'Pronisone', 'Prednisona', 'Predniment', 'Prednisonum', 'Rayos'}, 'medline_plus_id': 'a601102', 'mesh_id': 'D018931', 'drugbank_id': 'DB00635'}, 3, 3)]
```

You can ignore case with:

```
find_drugs("i bought some prednisone".split(" "), is_ignore_case=True)
```


# Interested in other kinds of named entity recognition (NER)? 💸Finances, 🎩company names, 🌎countries, 🗺️locations, proteins, 🧬genes, 🧪molecules?

If your NER problem is common across industries and likely to have been seen before, there may be an off-the-shelf NER tool for your purposes, such as our [Country Named Entity Recognition](http://fastdatascience.com//country-named-entity-recognition/) Python library. Dictionary-based named entity recognition is not always the solution, as sometimes the total set of entities is an open set and can't be listed (e.g. personal names), so sometimes a bespoke trained NER model is the answer. For tasks like finding email addresses or phone numbers, regular expressions (simple rules) are sufficient for the job.

If your named entity recognition or named entity linking problem is very niche and unusual, and a product exists for that problem, that product is likely to only solve your problem 80% of the way, and you will have more work trying to fix the final mile than if you had done the whole thing manually. Please [contact Fast Data Science](http://fastdatascience.com//contact) and we'll be glad to discuss. For example, we've worked on [a consultancy engagement to find molecule names in papers, and match author names to customers](http://fastdatascience.com//boehringer-ingelheim-finding-molecules-and-proteins-in-scientific-literature/) where the goal was to trace molecule samples ordered from a pharma company and identify when the samples resulted in a publication. For this case, there was no off-the-shelf library that we could use.

For a problem like identifying country names in English, which is a closed set with well-known variants and aliases, an off-the-shelf library is usually available. You may wish to try our [Country Named Entity Recognition](https://fastdatascience.com/country-named-entity-recognition/) library, also open-source and under MIT license.

For identifying a set of molecules manufactured by a particular company, this is the kind of task more suited to a [consulting engagement](https://fastdatascience.com/portfolio/nlp-consultant/).

# 😊 Using this tool directly from Google Sheets (no-code!)

<img align="left" alt="Google Sheets logo" title="Google Sheets logo" width=150 height=105  src="google_sheets_logo_small.png" />

We have a no-code solution where you can [use the library directly from Google Sheets](https://fastdatascience.com/drug-name-recogniser) as the library has also been wrapped as a Google Sheets plugin.

[Click here](https://www.youtube.com/watch?v=qab1Bv_YpYU) to watch a video of how the plugin works.

You can install the plugin in Google Sheets [here](https://workspace.google.com/marketplace/app/drug_name_recogniser/463844408236).

![google_sheets_screenshot.png](google_sheets_screenshot.png)

# Requirements

Python 3.9 and above

## ✉️Who to contact?

You can contact Thomas Wood or the Fast Data Science team at https://fastdatascience.com/.

# 🤝Compatibility with other natural language processing libraries

The Drug Named Entity Recognition library is independent of other NLP tools and has no dependencies. You don't need any advanced system requirements and the tool is lightweight. However, it combines well with other libraries  such as [spaCy](https://spacy.io) or the [Natural Language Toolkit (NLTK)](https://www.nltk.org/api/nltk.tokenize.html).

## Using Drug Named Entity Recognition together with spaCy

Here is an example call to the tool with a [spaCy](https://spacy.io) Doc object:

```
from drug_named_entity_recognition import find_drugs
import spacy
nlp = spacy.blank("en")
doc = nlp("i routinely rx rimonabant and pts prefer it")
find_drugs([t.text for t in doc], is_ignore_case=True)
```

outputs:

```
[({'name': 'Rimonabant', 'synonyms': {'Acomplia', 'Rimonabant', 'Zimulti'}, 'mesh_id': 'D063387', 'drugbank_id': 'DB06155'}, 3, 3)]
```

## Using Drug Named Entity Recognition together with NLTK

You can also use the tool together with the [Natural Language Toolkit (NLTK)](https://www.nltk.org/api/nltk.tokenize.html):

```
from drug_named_entity_recognition import find_drugs
from nltk.tokenize import wordpunct_tokenize
tokens = wordpunct_tokenize("i routinely rx rimonabant and pts prefer it")
find_drugs(tokens, is_ignore_case=True)
```

# 📁Data sources

The main data source is from Drugbank, augmented by datasets from the NHS, MeSH, Medline Plus and Wikipedia.

🌟 There is a handy Jupyter Notebook, `update.ipynb` which will update the Drugbank and MeSH data sources (re-download them from the relevant third parties). 

## Update the Drugbank dictionary

If you want to update the dictionary, you can use the data dump from Drugbank and replace the file `drugbank vocabulary.csv`:

* Download the open data dump from https://go.drugbank.com/releases/latest#open-data

## Update the Wikipedia dictionary

If you want to update the Wikipedia dictionary, download the dump from:

* https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia

and run `extract_drug_names_and_synonyms_from_wikipedia_dump.py`

## Update the MeSH dictionary

If you want to update the dictionary, run

```
python download_mesh_dump_and_extract_drug_names_and_synonyms.py
```

This will download the latest XML file from NIH.

If the link doesn't work, download the open data dump manually from https://www.nlm.nih.gov/. It should be called something like `desc2023.xml`. And comment out the Wget/Curl commands in the code.

## License information for external data sources

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

### 🤖 Continuous integration/deployment to PyPI

This package is based on the template https://pypi.org/project/example-pypi-package/

This package

- uses GitHub Actions for both testing and publishing
- is tested when pushing `master` or `main` branch, and is published when create a release
- includes test files in the source distribution
- uses **setup.cfg** for [version single-sourcing](https://packaging.python.org/guides/single-sourcing-package-version/) (setuptools 46.4.0+)

## 🧍Re-releasing the package manually

The code to re-release Harmony on PyPI is as follows:

```
source activate py311
pip install twine
rm -rf dist
python setup.py sdist
twine upload dist/*
```

## 😊 Who worked on the Drug Named Entity Recognition library?

The tool was developed:

* Thomas Wood ([Fast Data Science](https://fastdatascience.com))

## 📜License of Drug Named Entity Recognition library

MIT License. Copyright (c) 2023 [Fast Data Science](https://fastdatascience.com)

## ✍️ Citing the Drug Named Entity Recognition library

Wood, T.A., Drug Named Entity Recognition [Computer software], Version 1.0.10, accessed at [https://fastdatascience.com/drug-named-entity-recognition-python-library](https://fastdatascience.com/drug-named-entity-recognition-python-library), Fast Data Science Ltd (2024)

```
@unpublished{drugnamedentityrecognition,
    AUTHOR = {Wood, T.A.},
    TITLE  = {Drug Named Entity Recognition (Computer software), Version 1.0.10},
    YEAR   = {2024},
    Note   = {To appear},
    url = {https://zenodo.org/doi/10.5281/zenodo.10970631},
    doi = {10.5281/zenodo.10970631}
}
```
