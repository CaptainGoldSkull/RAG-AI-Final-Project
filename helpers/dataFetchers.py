import requests
import feedparser
import os
import zipfile

from bs4 import BeautifulSoup

#response = requests.get("https://cheatsheetseries.owasp.org/index.html")

#print(response.text)

owaspBaseLink = "https://cheatsheetseries.owasp.org/bundle.zip"
linkToParse = "https://cheatsheetseries.owasp.org/News.xml"

parsed = feedparser.parse(linkToParse)

    
def deepRemove(Path):
    # Recursive function that will go through a folder and remove all contents
    if os.path.isdir(Path):
        for fileName in os.listdir(Path):
            filePath = os.path.join(Path, fileName)
            if os.path.isdir(filePath):
                # Maybe need to add wait for return here...
                try:
                    print("Attemtping to remove directory.. "+ filePath)
                    os.rmdir(filePath)
                except:
                    print("Calling deepRemove on " + filePath)
                    deepRemove(filePath)
            elif os.path.isfile(filePath):
                print("Removing file " + filePath)
                os.remove(filePath)
        try:
            os.rmdir(filePath)
        except:
            print("Couldnt remove directory.. " + filePath)

def freshDownload(): # Use this for a fresh install/Complete refesh of data
    # Clear out any files in cachedPages
    #if len(os.listdir("cachedPages")) >= 1:
    for fileName in os.listdir("cachedPages"):
        # TO DO:
        # MAKE THIS WORK FIRST TIME.... Not all files get cleared
        print(fileName)
        filePath = os.path.join("cachedPages", fileName)
        if os.path.isdir(filePath):
            print("removign")
            try:
                os.rmdir(filePath)
            except:
                deepRemove(filePath)
    # Cache all the pages from download at:
    # https://cheatsheetseries.owasp.org/bundle.zip    

    requestedData = requests.get(owaspBaseLink)

    # Store a temporary zip fil;e in /temp
    with open("temp/owaspDelete.zip",mode="wb") as tempZip:
        tempZip.write(requestedData.content)

    # decompress into cachedPages/owasp
    with zipfile.ZipFile("temp/owaspDelete.zip", 'r') as zipRef:
        zipRef.extractall("cachedPages/owasp")
        
    # Remove temp zip
    os.remove("temp/owaspDelete.zip")

    # Next
    # Go through all the files created and strip them to "barebones"
    # Essentially just grab data-md-component="content" from the HTML
    # Then convert it to markdown?
    # ^ or just do .get_text() for it


def checkForUpdates():
    # Check the "last updated" compared to the files last modified for the page for each
    # Get this information from https://cheatsheetseries.owasp.org/News.xml
    # Download the data from the provided link
    print("Not meant to run yet")

