import os
from pinecone import Pinecone
from llama_index.core import StorageContext, VectorStoreIndex
from dotenv import load_dotenv

try:
    from llama_index.vector_stores.pinecone import PineconeVectorStore
except ModuleNotFoundError as e:
    raise ModuleNotFoundError(
        "Missing LlamaIndex Pinecone integration. Install `llama-index-vector-stores-pinecone`."
    ) from e


load_dotenv()


def get_pinecone_index(documents=None):
    # Initialize Pinecone
    api_key = os.getenv("PINECONE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing env var PINECONE_API_KEY")

    pc = Pinecone(api_key=api_key)

    index_name = os.getenv("PINECONE_INDEX_NAME", "medextract-index")
    index_host = os.getenv("PINECONE_INDEX_HOST")
    pinecone_index = pc.Index(host=index_host) if index_host else pc.Index(index_name)
    
    # Initialize the Vector Store
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    
    if documents:
        # Uploading data for the first time
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        return VectorStoreIndex.from_documents(
            documents, storage_context=storage_context
        )
    else:
        # Just loading the existing index
        return VectorStoreIndex.from_vector_store(vector_store=vector_store)


def get_retriever():
    # Connects to Pinecone instead of local index
    index = get_pinecone_index()
    return index.as_retriever(similarity_top_k=3)

