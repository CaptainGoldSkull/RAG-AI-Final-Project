from bs4 import BeautifulSoup
from html_to_markdown import convert
import os

# Functions that can be called on a html file to "Strip" it

runCount = 0
maxRetries = 5

def cleanOwaspFiles():
    # Get the data from <div class="md-content" data-md-component="content"> section of the html segment
    # Save on storage & vectorspace size etc only keep important info
    pathToCleanse = "cachedPages/owasp/site/cheatsheets"
    if os.path.isdir(pathToCleanse):
        for fileName in os.listdir(pathToCleanse):
            filePath = pathToCleanse+"/"+fileName
            if os.path.isfile(filePath):
                with open(filePath,mode="r") as fileToRead:
                    soup = BeautifulSoup(fileToRead,'html.parser')
                    actualPageContent = soup.find("div","md-content")
                    #actualPageContent = actualPageContent.get_text() <-- Use if you wanna use text as output for processed but im going to use markdown
                    actualPageContent = convert(str(actualPageContent))
                    #print(filePath)

                    with open("processedHtml/"+fileName[:-4]+"md",mode="w") as processedFile:
                        processedFile.write(actualPageContent)
    else:
        if runCount < maxRetries:
            # TO DO:
            # Add in "corrupt" data handling i.e check if there are actually files for it to cleanse and re download if there isnt... perhaps something cooler later
            print(f"error finding cachedPages file. Attempt: {runCount} out of {maxRetries}. {maxRetries-runCount} attempts left...  Retrying")
