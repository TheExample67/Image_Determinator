import urllib.request
import requests
from bs4 import BeautifulSoup
import json
import os

DATADIR ="data"
ToChecks = []
NumberOfSiteToCheck = 10
with open("data\SourceData.json","r") as Source:
    datastore = json.load(Source)
    ToChecks = datastore["CheckData"]

i = 1
for ToCheck in ToChecks:
    directory = os.path.join(DATADIR,ToCheck["type"])

    try:
        os.stat(directory)
    except:
        os.mkdir(directory)

    baseURL = ToCheck["URL"]
    for a in range(1,NumberOfSiteToCheck):
        page = requests.get(baseURL.format(str(a)))

        soup = BeautifulSoup(page.content,'html.parser')
        results = soup.find_all('img')
        for result in results:
            if result.has_attr("data-lazy"):
                url = result["data-lazy"]       
            if result.has_attr("src"):
                url = result['src']
            if url.startswith("http"):
                filepath = directory 
                fn = directory + "\img_{0}.jpg".format(str(i))
                response = requests.get(url)
                if response.status_code == 200:
                    img_data = response.content
                    with open(fn, 'wb') as handler:
                        handler.write(img_data)
            i += 1
