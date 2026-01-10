from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from dotenv import load_dotenv
from langchain_groq import ChatGroq

import os


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
    #print(docSplit)
    for split_doc in docSplit:
        split_doc.metadata["source"] = doc.metadata["source"]
    
    chunks.extend(docSplit)
    

# MOVE EMBEDDINGS AND CHROMA TO ITS OWN SECTION LATER
    
embeddings_model = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
persistent_db_path = "db8"

db_client = Chroma(persist_directory=persistent_db_path, embedding_function=embeddings_model)
    
batch_size = 5000 # Using a batch size that is less than the max_batch_size of 5461
update_every = 25
total = len(chunks)
for i in range(0, total, batch_size):
    batch = chunks[i:i + batch_size]
    db_client.add_documents(batch)
    if i % update_every == 0:
        print(f"Indexed {i}/{total} chunks")


def with_RAG(user_query, k = 5, style = "formal", language= "english"):
    load_dotenv()

    groqKey = os.getenv("GROQ_API_KEY")
    if not groqKey:
        raise RuntimeError("GROQ_API_KEY not set")
    llm = ChatGroq(api_key="groqKey",model="llama-3.1-8b-instant", temperature=0)

    retrieved_docs = db_client.similarity_search(query=user_query, k=k)
    retrieved_docs_text = [doc.page_content for doc in retrieved_docs]
    retrieved_docs_text_str = "\n".join(retrieved_docs_text)

    query_and_context = (
        "These docs can help you with your questions. If you have no answer, simply say 'I do not know'."
        f"Question: {user_query}\n"
        f"Relevant docs: {retrieved_docs_text_str}"
    )

    messages = [
        ("system", f"You are an expert assistant providing information strictly based on the context provided to you. Your task is to answer questions or provide information only using the details given in the current context. Do not reference any external knowledge or information not explicitly mentioned in the context. If the context does not contain sufficient information to answer a question, clearly state that the information is not available in the provided context. You should answer in a {style} style and in {language} language."),
        ("human", query_and_context)
    ]

    res = llm.invoke(messages)
    return res.content


print(with_RAG("What is a security measure that artificial intelligence agents should implement?"))