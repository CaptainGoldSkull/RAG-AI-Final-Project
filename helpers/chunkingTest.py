from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


embeddings_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


recursive_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 100,
    chunk_overlap  = 50,
    separators=["\n\n","\n"," ", ""],
    add_start_index = True,
)




with open("processedHtml/AI_Agent_Security_Cheat_Sheet.html") as docToProcess:
    doc_texts = recursive_text_splitter.split_documents(docToProcess)

texts=[doc.page_content for doc in doc_texts]
print(f'Number of Chunks after splitting: {len(texts)}')

embeds= embeddings_model.embed_documents(texts)
print(f'Number of Embeddings: {len(embeds)}')
print(f'Length of the embeddings vectors:{len(embeds[0])}')

print(f"Original Text: {doc_texts}\n")
print(f"Number of Chunks: {len(doc_texts)}\n")
for i, doc in enumerate(doc_texts):
    print(f"Chunk {i+1}:")
    print(doc.page_content)
    print(embeds[i])
    print("-" * 20)


print("executed")