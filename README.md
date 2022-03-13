# drugfinder

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