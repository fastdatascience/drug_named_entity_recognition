import pandas as pd
import re
import operator
import csv
import drugs_finder
import xml.sax
import subprocess
import datetime
from sys import platform
import os

# Example URL of MeSH dump: https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/desc2023.xml

mesh_xml_file_name = f"desc{datetime.datetime.now().year}.xml"
url = f"https://nlmpubs.nlm.nih.gov/projects/mesh/MESH_FILES/xmlmesh/{mesh_xml_file_name}"

if os.path.exists(mesh_xml_file_name):
    print (f"Removing old XML file {mesh_xml_file_name}.")
    os.remove(mesh_xml_file_name)
  
print (f"Downloading MeSH XML dump from {url}. If this URL doesn't work, please navigate to https://www.nlm.nih.gov/ and search the site for a MeSH data dump in XML format.")

print (f"Platform is {platform}.")
if "win" in platform: # if we are on Windows, use curl.exe (supported in Windows 10 and up)
    wget = subprocess.Popen(["curl.exe", "--output", mesh_xml_file_name, "--url", url])
else:
    wget = subprocess.Popen(["wget", url])

os.waitpid(wget.pid, 0)
                        
print (f"Downloaded MeSH XML dump from {url}.")

IMPORTANT_TAGS = {'DescriptorName', 'String', 'DescriptorUI', 'DescriptorRecord', 'TreeNumber', 'Term'}

# define a Custom ContentHandler class that extends ContenHandler
class CustomContentHandler(xml.sax.ContentHandler):
    def __init__(self, writer):
        self.writer = writer
        self.writer.writerow(["Mesh ID", "Common name", "Synonyms"])
        self.postCount = 0
        self.entryCount = 0
        self.is_in = dict([n, False] for n in IMPORTANT_TAGS)
        self.title = ""
        self.id = ""
        self.tree_numbers = set()
        self.terms = set()
        self.path = []

    # Handle startElement
    def startElement(self, tagName, attrs):
        self.path.append(tagName)
        if tagName in IMPORTANT_TAGS:
            self.is_in[tagName] = True

    # Handle endElement
    def endElement(self, tagName):
        if tagName != self.path[-1]:
            1/0
        self.path = self.path[:-1]
        if tagName == "DescriptorRecord":
            #if True or self.title.upper() in drugs_finder.drug_variant_to_canonical:
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
            if not self.title.upper() in drugs_finder.drug_variant_to_canonical:
                is_include = False
            if is_include:
                self.writer.writerow([self.id, self.title, "|".join(self.terms)])
                print (self.id, self.title, self.tree_numbers, self.terms)
            self.title = ""
            self.id = ""
            self.tree_numbers = set()
            self.terms = set()

        if tagName in IMPORTANT_TAGS:
            self.is_in[tagName] = False


    # Handle text data
    def characters(self, chars):
        if self.is_in["DescriptorName"] and self.is_in["String"]:
            if "/".join(self.path) == "DescriptorRecordSet/DescriptorRecord/DescriptorName/String":
                self.title += chars
        if self.is_in["Term"] and self.is_in["String"]:
            self.terms.add(chars)
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
