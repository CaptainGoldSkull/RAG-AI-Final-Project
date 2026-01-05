from bs4 import BeautifulSoup

# Functions that can be called on a html file to "Strip" it

def extractOWASPCheatSheet(filePath):
    # Get the data from <div class="md-content" data-md-component="content"> section of the html segment
    # Save on storage & vectorspace size etc only keep important info
    with open(filePath,mode="r") as fileToRead:
        soup = BeautifulSoup(fileToRead,'html.parser')
        actualPageContent = soup.find("div","md-content")
        actualPageContent = actualPageContent.get_text()
        print(actualPageContent)
extractOWASPCheatSheet("cachedPages/owasp/site/cheatsheets/XML_Security_Cheat_Sheet.html")