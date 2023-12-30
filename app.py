import os
from dotenv import load_dotenv
import openai
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Milvus
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import DirectoryLoader



embed_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L12-v2")





text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
doc_splits = text_splitter.split_documents(documents.load())
print(len(doc_splits))

# Set up a vector store used to save the vector embeddings. Here we use Milvus as the vector store.
vector_store = Milvus.from_documents(
    doc_splits,
    embedding=embed_model,
    connection_args={"host": "localhost", "port": 19530}, collection_name="wiki"
)
