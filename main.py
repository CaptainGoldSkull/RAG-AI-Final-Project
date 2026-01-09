import os 
import typer # used for CLI implementation

from helpers.dataFetchers import *
from helpers.textProcessing import *

def main():
    
    if len(os.listdir("cachedPages")) < 1:
        print("No cached pages... Caching")
        freshDownload()
    
    if len(os.listdir("processedHtml")) < 1:
        if len(os.listdir("cachedPages/owasp")) >= 1:
            cleanOwaspFiles()
        


if __name__ == "__main__":
    typer.run(main)

