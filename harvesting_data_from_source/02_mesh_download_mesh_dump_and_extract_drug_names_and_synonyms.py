
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

import csv
import datetime
import os
import subprocess
import xml.sax
from sys import platform

# Example URL of MeSH dump: https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2023.xml

mesh_xml_file_name = f"desc{datetime.datetime.now().year}.xml"
url = f"https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/{mesh_xml_file_name}"

if os.path.exists(mesh_xml_file_name):
    print(f"Removing old XML file {mesh_xml_file_name}.")
    os.remove(mesh_xml_file_name)

print(
    f"Downloading MeSH XML dump from {url}. If this URL doesn't work, please navigate to https://www.nlm.nih.gov/ and search the site for a MeSH data dump in XML format.")

print(f"Platform is {platform}.")
if "win" in platform:  # if we are on Windows, use curl.exe (supported in Windows 10 and up)
    wget = subprocess.Popen(["curl.exe", "--output", mesh_xml_file_name, "--url", url])
else:
    wget = subprocess.Popen(["wget", url])

os.waitpid(wget.pid, 0)

print(f"Downloaded MeSH XML dump from {url}.")

IMPORTANT_TAGS = {'DescriptorName', 'String', 'DescriptorUI', 'DescriptorRecord', 'TreeNumber', 'Term'}


# define a Custom ContentHandler class that extends ContenHandler
class CustomContentHandler(xml.sax.ContentHandler):
    def __init__(self, writer):
        self.writer = writer
        self.writer.writerow(["Mesh ID", "Generic name", "Common name", "Synonyms", "Tree"])
        self.postCount = 0
        self.entryCount = 0
        self.is_in = dict([n, False] for n in IMPORTANT_TAGS)
        self.title = ""
        self.id = ""
        self.tree_numbers = set()
        self.terms = set()
        self.generic_names = set()
        self.path = []
        self.RecordPreferredTermYN = ""

    # Handle startElement
    def startElement(self, tagName, attrs):
        self.path.append(tagName)
        if tagName == 'Term':
            if "RecordPreferredTermYN" in attrs.getNames():
                self.RecordPreferredTermYN = attrs.getValue("RecordPreferredTermYN")
        if tagName in IMPORTANT_TAGS:
            self.is_in[tagName] = True

    # Handle endElement
    def endElement(self, tagName):
        self.path = self.path[:-1]
        if tagName == "Term":
            self.RecordPreferredTermYN = ""
        if tagName == "DescriptorRecord":
            # if True or self.title.upper() in drugs_finder.drug_variant_to_canonical:
            is_include = False
            for t in self.tree_numbers:
                if t.startswith("D"):
                    is_include = True
                else:
                    is_include = False
                    break
                if len(t.split('.')) < 4:
                    is_include = False
                    break
            if is_include:
                self.writer.writerow([self.id, "|".join(self.generic_names), self.title, "|".join(self.terms), "|".join(self.tree_numbers)])
                # print(self.id, self.title, self.tree_numbers, self.terms)
            self.title = ""
            self.id = ""
            self.tree_numbers = set()
            self.terms = set()
            self.generic_names = set()

        if tagName in IMPORTANT_TAGS:
            self.is_in[tagName] = False

    # Handle text data
    def characters(self, chars):
        if self.is_in["DescriptorName"] and self.is_in["String"]:
            if "/".join(self.path) == "DescriptorRecordSet/DescriptorRecord/DescriptorName/String":
                self.title += chars
        if self.is_in["Term"] and self.is_in["String"]:
            self.terms.add(chars)
            if self.RecordPreferredTermYN == "Y":
                self.generic_names.add(chars)
        if self.is_in["DescriptorUI"]:
            self.id = chars
        if self.is_in["TreeNumber"]:
            self.tree_numbers.add(chars)

    # Handle startDocument
    def startDocument(self):
        print('About to start!')

    # Handle endDocument
    def endDocument(self):
        print('Finishing up!')


with open("drugs_dictionary_mesh.csv", "w", encoding="utf-8") as fo:
    writer = csv.writer(fo)

    handler = CustomContentHandler(writer)
    xml.sax.parse(mesh_xml_file_name, handler)
