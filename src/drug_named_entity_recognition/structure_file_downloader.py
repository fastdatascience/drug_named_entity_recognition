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
import pathlib
import re
import subprocess
import zipfile
from sys import platform

import requests


def download_structures(this_path):
    temp_mirror_url = 'https://fastdatascience.z33.web.core.windows.net/drugbank_all_open_structures.sdf.zip'

    if not temp_mirror_url:
        response = requests.get("https://go.drugbank.com/releases/latest#open-data")

        re_url = re.compile(r'\bhttps://go.drugbank.com/releases/[a-z0-9-/]+all-open-structures\b')

        url = re_url.findall(response.text)[0]
    else:
        url = temp_mirror_url

    print(f"URL to download structured data from on Drugbank is {url}")

    # To avoid too much traffic to Drugbank, we download molecule structure data from the mirror at Fast Data Science
    url = 'https://fastdatascience.z33.web.core.windows.net/drugbank_all_open_structures.sdf.zip'

    print(f"Downloading from Fast Data Science mirror {url}...")

    print(f"Platform is {platform}.")
    if "win" in platform:  # if we are on Windows, use curl.exe (supported in Windows 10 and up)
        tmpfile = "C:/temp/tmp.zip"
        wget = subprocess.Popen(["curl.exe", "--output", tmpfile, "--url", url])
    else:
        tmpfile = "/tmp/tmp.zip"
        wget = subprocess.Popen(["wget", "-O", tmpfile, url])

    os.waitpid(wget.pid, 0)

    print(f"Downloaded Drugbank dump from {url} to {tmpfile}.")

    with zipfile.ZipFile(tmpfile, 'r') as zip_ref:
        zip_ref.extractall(str(this_path))
    #
    #
    # if "win" in platform:  # if we are on Windows, use curl.exe (supported in Windows 10 and up)
    #     unzip = subprocess.Popen(["unzip", -"o", tmpfile, "-d", str(this_path)])
    # else:
    #     unzip = subprocess.Popen(["unzip", "-o", tmpfile, "-d", str(this_path)])
    #
    # os.waitpid(unzip.pid, 0)

    print(f"Unzipped Drugbank dump from {tmpfile} to directory {this_path}.")


if __name__ == "__main__":
    this_path = pathlib.Path(__file__).parent.resolve()

    download_structures(this_path)
