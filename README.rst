Drug named entity recognition
=============================

Developed by Fast Data Science, https://fastdatascience.com

Source code at
https://github.com/fastdatascience/drug_named_entity_recognition

This is a lightweight Python library for finding drug names in a string.

Please note this library finds only high confidence drugs.

It also only finds the English names of these drugs. Names in other
languages are not supported.

It also doesn’t find short code names of drugs, such as abbreviations
commonly used in medicine, such as “Ceph” for “Cephradin” - as these are
highly ambiguous.

Requirements
============

Python 3.9 and above

Installation
============

::

   pip install drug-named-entity-recognition

Usage examples
==============

You must first tokenise your input text using a tokeniser of your choice
(NLTK, spaCy, etc).

You pass a list of strings to the ``find_drugs`` function.

Example 1

::

   from drug_named_entity_recognition import find_drugs

   find_drugs("i bought some Phenoxymethylpenicillin".split(" "))

outputs a list of tuples.

::

   [({'name': 'Phenoxymethylpenicillin',
      'synonyms': {'Penicillin', 'Phenoxymethylpenicillin'},
      'nhs_url': 'https://www.nhs.uk/medicines/phenoxymethylpenicillin',
      'drugbank_id': 'DB00417'},
     3,
     3)]

You can ignore case with:

::

    find_drugs("i bought some phenoxymethylpenicillin".split(" "), is_ignore_case=True)

Data sources
============

The main data source is from Drugbank, augmented by datasets from the
NHS, MeSH, Medline Plus and Wikipedia.

Update the Drugbank dictionary
------------------------------

If you want to update the dictionary, you can use the data dump from
Drugbank and replace the file ``drugbank vocabulary.csv``:

-  Download the open data dump from
   https://go.drugbank.com/releases/latest#open-data

Update the Wikipedia dictionary
-------------------------------

If you want to update the Wikipedia dictionary, download the dump from:

-  https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia

and run ``extract_drug_names_and_synonyms_from_wikipedia_dump.py``

Update the MeSH dictionary
--------------------------

If you want to update the dictionary, download the open data dump from
https://www.nlm.nih.gov/

and run ``extract_drug_names_and_synonyms_from_mesh_dump.py``