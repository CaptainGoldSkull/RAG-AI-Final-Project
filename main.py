import os 
import typer # used for CLI implementation

from helpers.dataFetchers import *

def main():
    
    if len(os.listdir("cachedPages")) < 1:
        print("No cached pages... Caching")
        freshDownload()
    


if __name__ == "__main__":
    typer.run(main)

