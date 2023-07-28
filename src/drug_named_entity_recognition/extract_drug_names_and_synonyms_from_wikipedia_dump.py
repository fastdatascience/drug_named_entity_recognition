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


