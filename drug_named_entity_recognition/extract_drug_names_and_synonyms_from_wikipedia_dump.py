#!/usr/bin/env python
# coding: utf-8

# Get trade names from Wikipedia dump
# If you want to update the Wikipedia drugs dictionary, you need to download the dump of English Wikipedia from:
# https://meta.wikimedia.org/wiki/Data_dump_torrents#English_Wikipedia
# 
# The dump is 20 GB compressed so you need to read it as a Bzip file.

import bz2
import os
import urllib.parse, csv

current_title =None
is_in_clinical = 0
found = []

bytes_read = 0

source_file = bz2.BZ2File("enwiki-20220101-pages-articles-multistream.xml.bz2", "r")
for line in source_file:
    '''
    l = line.decode("iso-8859-1").strip()
    if "<title>" in l:
            current_title = l
    if "-- Clinical data --" in l:
        is_in_clinical = 10
    '''
    bytes_read += len(line)
    
    if line.find(b'<title>') >= 0:
        current_title = line
    elif line.find(b'-- Clinical data --') >= 0:
        is_in_clinical = 10
    elif is_in_clinical > 0 and line.find(b'| tradename') >= 0:
        found.append((current_title.decode("iso-8859-1").strip(), line.decode("iso-8859-1").strip()))

    is_in_clinical -= 1
    
    if bytes_read % 100000000 < 2000:
        os.system('cls||clear')
        print ("num gigabytes seen", bytes_read / 1000000000)


with open("drugs_dictionary_wikipedia.csv", "w", encoding="utf-8") as fo:
    writer = csv.writer(fo)
    writer.writerow(["Wikipedia link", "Common name", "Synonyms"])
    
    import re
    for title, tradenames in found:
        title = re.sub(r'^.*<title>|</title.*$', '', title)
        tradenames = re.sub(r"(?i)^.*tradename *=|\b(many|others|and other|hundreds).*$", "", tradenames)
        tradenames = re.sub(r'\[\[.+?\|', '', tradenames)
        tradenames = re.sub(r'\]\]', '', tradenames)
        tradenames = re.sub(r',$', '', tradenames.strip())
        print (title, "/",  tradenames)
        
        synonyms = "|".join([t.strip() for t in tradenames.split(",")])
        
        link = 'https://en.wikipedia.org/wiki/' + urllib.parse.quote(title.encode('utf8'))
        
        writer.writerow([link, title, synonyms])


