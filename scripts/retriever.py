import os
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.pinecone import PineconeVectorStore
from dotenv import load_dotenv

def get_retriever():
    # Initialize Pinecone
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing env var PINECONE_API_KEY")

    pc = Pinecone(api_key=api_key)
    index_name = os.getenv("PINECONE_INDEX_NAME", "medextract-index")
    index_host = os.getenv("PINECONE_INDEX_HOST")
    pinecone_index = pc.Index(host = index_host, name = index_name)
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index.as_retriever(similarity_top_k=3)