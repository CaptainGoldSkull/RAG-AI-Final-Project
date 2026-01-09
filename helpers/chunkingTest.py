from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader


dirLoader = DirectoryLoader(
    "processedHtml/",
    glob="**.md",
    loader_cls=TextLoader,
)

headersToSplit = [
    ("#", "Header 1"),
    ("##", "Header 2"),
    #("###", "Header 3"),
]
markdownSplitter = MarkdownHeaderTextSplitter(headersToSplit)

docs_iter = dirLoader.lazy_load()

chunks = []
for doc in docs_iter:
    
    docSplit = markdownSplitter.split_text(doc.page_content)
    print(docSplit)
    for split_doc in docSplit:
        split_doc.metadata["source"] = doc.metadata["source"]
    
    chunks.extend(docSplit)
    
    embeddings_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")


    persistent_db_path = "db8"

    db_client = Chroma(persist_directory=persistent_db_path, embedding_function=embeddings_model)
    
    batch_size = 5000 # Using a batch size that is less than the max_batch_size of 5461
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        db_client.add_documents(batch)






print(chunks)

# Use this to set max chunk size when i know what the limits of the model im going to use are.
chunk_size = 250
chunk_overlap = 30
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size, chunk_overlap=chunk_overlap
)

# Split
#splits = text_splitter.split_documents(md_header_splits)




#print(md_header_splits)
