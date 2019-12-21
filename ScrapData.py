import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import os
import tarfile

DATADIR ="data"
SOURCEDIR = "source"
ToChecks = []
NumberOfSiteToCheck = 10
with open("SourceData.json","r") as Source:
    datastore = json.load(Source)
    ToChecks = datastore["SearchWebsite"]

i = 1
for ToCheck in ToChecks:
    searchValues = ToCheck["searchTags"]
    for searchValue in searchValues:
        directory = os.path.join(SOURCEDIR,searchValue)

        try:
            os.stat(directory)
        except:
            os.mkdir(directory) 
        for a in range(1,NumberOfSiteToCheck + 1):
            url = ToCheck["baseURL"].format(searchValue,str(a))
            print(url)   
            response = requests.get(url)
            soup = BeautifulSoup(response.content,"html.parser")
            images_found = soup.find_all("img")
            for image_found in images_found:
                if image_found.has_attr("data-lazy"):
                    downloadurl = image_found["data-lazy"]
                if image_found.has_attr("src"):
                    downloadurl = image_found["src"]
                if downloadurl.startswith("http"):
                    img_response = requests.get(downloadurl)
                    if img_response.status_code == 200:
                        img_data = img_response.content
                        with open(directory + "\img_{0}.jpg".format(str(i)), "wb") as img_file:
                            img_file.write(img_data)
                i += 1


def tardir(_SOURCEDIR, tar_name):
    with tarfile.open(tar_name, "w:gz") as tar_handle:
        for root, dirs, files in os.walk(_SOURCEDIR):
            for file in files:
                tar_handle.add(os.path.join(root, file))
tardir(SOURCEDIR, DATADIR+'\sample.tar.gz')

