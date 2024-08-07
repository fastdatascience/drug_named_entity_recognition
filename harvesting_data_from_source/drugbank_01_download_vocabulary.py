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

import os
import re
import subprocess
from sys import platform

import requests

response = requests.get("https://go.drugbank.com/releases/latest#open-data")

re_url = re.compile(r'\bhttps://go.drugbank.com/releases/[a-z0-9-/]+all-drugbank-vocabulary\b')

url = re_url.findall(response.text)[0]

print(f"Platform is {platform}.")
if "win" in platform:  # if we are on Windows, use curl.exe (supported in Windows 10 and up)
    tmpfile = "C:/temp/tmp.zip"
    wget = subprocess.Popen(["curl.exe", "--output", tmpfile, "--url", url])
else:
    tmpfile = "/tmp/tmp.zip"
    wget = subprocess.Popen(["wget", "-O", tmpfile, url])

os.waitpid(wget.pid, 0)

print(f"Downloaded Drugbank dump from {url} to {tmpfile}.")

if "win" in platform:  # if we are on Windows, use curl.exe (supported in Windows 10 and up)
    unzip = subprocess.Popen(["unzip", -"o", tmpfile, "-d", "."])
else:
    unzip = subprocess.Popen(["unzip", "-o", tmpfile, "-d", "."])

os.waitpid(unzip.pid, 0)

print(f"Unzipped Drugbank dump from {tmpfile} to current directory.")
