from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma


def chromaEmbedding(chunksToEmbed):        
    batch_size = 5000 
    update_every = 25
    total = len(chunksToEmbed)
    for i in range(0, total, batch_size):
        batch = chunksToEmbed[i:i + batch_size]
        getDBClient().add_documents(batch)
        if i % update_every == 0:
            print(f"Indexed {i}/{total} chunks")

def getDBClient():
    embeddings_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    persistent_db_path = "db8"

    db_client = Chroma(persist_directory=persistent_db_path, embedding_function=embeddings_model)
    return db_client
# MOVE EMBEDDINGS AND CHROMA TO ITS OWN SECTION LATER
    


