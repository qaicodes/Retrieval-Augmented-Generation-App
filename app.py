import os
from dotenv import load_dotenv
import openai
from llama_index.vector_stores import MilvusVectorStore
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index import SimpleDirectoryReader, VectorStoreIndex, StorageContext, ServiceContext
from llama_index.query_engine import CitationQueryEngine

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
ZILLIZ_URI = os.getenv("ZILLIZ_CLUSTER_01_URI")
ZILLIZ_TOKEN = os.getenv("ZILLIZ_CLUSTER_01_TOKEN")


vdb = MilvusVectorStore(
    uri = ZILLIZ_URI,
    token = ZILLIZ_TOKEN,
    collection_name = "breaking_bad",
    dim = 384
)

embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L12-v2")


storage_context = StorageContext.from_defaults(vector_store=vdb)
service_context = ServiceContext.from_defaults(embed_model=embed_model)

documents = SimpleDirectoryReader("./halloween_data/").load_data()

vector_index = VectorStoreIndex.from_documents(documents, storage_context=storage_context, service_context=service_context)



query_engine = CitationQueryEngine.from_args(
    vector_index,
    similarity_top_k=3,
    # here we can control how granular citation sources are, the default is 512
    citation_chunk_size=512,
)

response = query_engine.query("Who is the main character?")
for source in response.source_nodes:
    print(source.node.get_text())