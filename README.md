# drugfinder

The main data source is from Drugbank. 

This is augmented by datasets from the NHS and Medline Plus and Wikipedia.

If you want to update the dictionary, you can use the data dump from Drugbank and replace the file `drugbank vocabulary.csv`:

* Download the open data dump from https://go.drugbank.com/releases/latest#open-data

If you want to update the Wikipedia dictionary, download the dump from:

https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia

and run `extract_drug_names_and_synonyms_from_wikipedia_dump.py`
