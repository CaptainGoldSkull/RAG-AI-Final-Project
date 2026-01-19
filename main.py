import os 
import typer # used for CLI implementation

from helpers.dataFetchers import *
from helpers.textProcessing import *
from helpers.embedding import *

from langchain_groq import ChatGroq
from dotenv import load_dotenv

groqKey = os.getenv("GROQ_API_KEY")

def query(user_query, k = 5, style = "formal", language= "english"):
    load_dotenv(dotenv_path=".env", override=True)

       
    llm = ChatGroq(api_key=groqKey,model="llama-3.1-8b-instant", temperature=0)

    dbClient = getDBClient()
    retrieved_docs = dbClient.similarity_search(query=user_query, k=k)
    retrieved_docs_text = [doc.page_content for doc in retrieved_docs]
    retrieved_docs_text_str = "\n".join(retrieved_docs_text)

    query_and_context = (
        "You have been provided with OWASP cheat sheet documentation to help with any questions the user gives you. If you have no answer, simply say 'I do not know'."
        f"Question: {user_query}\n"
        f"Relevant docs: {retrieved_docs_text_str}"
    )

    messages = [
        ("system", f"You are a cyber security research tool. Answer the question is as much detail as possible and provide sources with links to the document you get the information from. Answer in a {style} tone and in {language}."),
        ("human", query_and_context)
    ]

    res = llm.invoke(messages)
    return res.content



def main():

    if not groqKey:
        raise RuntimeError(f'GROQ_API_KEY not set \n Please create a .env file with a value called GROQ_API_KEY \n i.e GROQ_API_KEY="APIKEYHERE", Keys can be made for free here: \n https://console.groq.com/home')
    
    if len(os.listdir("cachedPages")) < 1:
        print("No cached pages... Caching")
        freshDownload()
    
    if len(os.listdir("processedHtml")) < 1:
        if len(os.listdir("cachedPages/owasp")) >= 1:
            cleanOwaspFiles()
    if not os.path.exists("db8") or len(os.listdir("db8")) < 1:
        chromaEmbedding(splitPage())


    questionToAsk = input(f"What is your query for the OWASP database?. \n")
    print(query(questionToAsk))



if __name__ == "__main__":
    typer.run(main)

