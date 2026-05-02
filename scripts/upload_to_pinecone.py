import os

from dotenv import load_dotenv
from pinecone import Pinecone
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores.pinecone import PineconeVectorStore

load_dotenv()

def upload_narratives_to_pinecone(directory_path="data/processed_narratives/"):
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    if not pinecone_api_key:
        raise RuntimeError("Missing env var PINECONE_API_KEY")

    # LlamaIndex will embed your documents during upload; default setup typically needs OpenAI.
    # If you see embedding/LLM errors, set OPENAI_API_KEY or configure a different embed model.
    if not os.getenv("OPENAI_API_KEY"):
        print("Warning: OPENAI_API_KEY is not set. Upload may fail during embedding.")

    # Initialize Pinecone client
    pc = Pinecone(api_key=pinecone_api_key)
    
    # Connect to Pinecone index
    index_name = os.getenv("PINECONE_INDEX_NAME", "medextract-index")
    index_host = os.getenv("PINECONE_INDEX_HOST")
    pinecone_index = pc.Index(index_name, host=index_host or "")
    
    # Set up the Vector Store & Storage Context
    vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    # Load documents from your processed folder
    print(f"Reading narratives from {directory_path}")
    documents = SimpleDirectoryReader(directory_path).load_data()
    
    # Create Index and upload to Pinecone
    print(f"Found {len(documents)} documents. Starting upload to Pinecone...")
    index = VectorStoreIndex.from_documents(
        documents, 
        storage_context=storage_context,
        show_progress=True
    )
    
    print("Successfully uploaded all clinical narratives to Pinecone!")

if __name__ == "__main__":
    upload_narratives_to_pinecone()