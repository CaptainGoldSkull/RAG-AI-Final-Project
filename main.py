import os 
import typer # used for CLI implementation


def main():
    if len(os.listdir("cachedPages")) < 1:
        print("No cached pages... Caching")


if __name__ == "__main__":
    typer.run(main)

#print(len(os.listdir("cachedPages")))