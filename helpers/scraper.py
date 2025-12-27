import requests
import feedparser
import os
import zipfile

#response = requests.get("https://cheatsheetseries.owasp.org/index.html")

#print(response.text)

owaspBaseLink = "https://cheatsheetseries.owasp.org/bundle.zip"
linkToParse = "https://cheatsheetseries.owasp.org/News.xml"

parsed = feedparser.parse(linkToParse)


def freshDownload(): # Use this for a fresh install/Complete refesh of data
    # Clear out any files in cachedPages
    # Re-Cache all the pages from download at:
    # https://cheatsheetseries.owasp.org/bundle.zip
    if len(os.listdir("cachedPages")) > 1:
        print("I need to add a clear function in here")
    

    requestedData = requests.get(owaspBaseLink)

    with open("temp/owaspDelete.zip",mode="wb") as tempZip:
        tempZip.write(requestedData.content)

    with zipfile.ZipFile("temp/owaspDelete.zip", 'r') as zipRef:
        zipRef.extractall("cachedPages/owasp")
        
    os.remove("temp/owaspDelete.zip")

    
def checkForUpdates():
    # Check the "last updated" compared to the files last modified for the page for each
    # Get this information from https://cheatsheetseries.owasp.org/News.xml
    # Download the data from the provided link
    print("Not meant to run yet")

freshDownload()