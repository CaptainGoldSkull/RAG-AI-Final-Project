from bs4 import BeautifulSoup
from html_to_markdown import convert


from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader

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


def splitPage():
    dirLoader = DirectoryLoader(
        "processedHtml/",
        glob="**.md",
        loader_cls=TextLoader,
    )

    headersToSplit = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdownSplitter = MarkdownHeaderTextSplitter(headersToSplit)

    size_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=120,
        separators=["\n\n", "\n", " ", ""],
    )

    docs_iter = dirLoader.lazy_load()
    chunks = []
    for doc in docs_iter:
        
        docSplit = markdownSplitter.split_text(doc.page_content)
        #print(docSplit)
        recursiveSplit = size_splitter.split_documents(docSplit) # This is done as with just markdown split tokens still reach max size occasionally
        for split_doc in recursiveSplit:
            split_doc.metadata["source"] = doc.metadata["source"]
            
        chunks.extend(recursiveSplit)
    return chunks



