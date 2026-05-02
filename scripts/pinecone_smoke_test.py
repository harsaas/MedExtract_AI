import os

from vectorstore import get_pinecone_index


def main() -> int:
    # 1) Load Pinecone-backed LlamaIndex index
    try:
        index = get_pinecone_index()
    except Exception as e:
        print("Failed to initialize Pinecone/LlamaIndex index.")
        print(f"Error: {type(e).__name__}: {e}")
        print("\nChecklist:")
        print("- Set PINECONE_API_KEY in your .env")
        print("- Set PINECONE_INDEX_NAME=medextract-index (optional)")
        print("- Set PINECONE_INDEX_HOST from Pinecone console (recommended)")
        return 1

    print("Loaded VectorStoreIndex from Pinecone.")

    # 2) Try a query
    query_text = os.getenv("SMOKE_TEST_QUERY", "What is this index about?")
    print(f"\nQuery: {query_text}")

    try:
        query_engine = index.as_query_engine(similarity_top_k=3)
        response = query_engine.query(query_text)
        print("\nResponse:")
        print(str(response))
        return 0
    except Exception as e:
        print("\nIndex loaded, but query failed.")
        print(f"Error: {type(e).__name__}: {e}")
        print("\nCommon causes:")
        print("- Missing OPENAI_API_KEY (if your LlamaIndex defaults use OpenAI)")
        print("- Embedding dimension mismatch vs the Pinecone index")
        print("- Missing llama-index OpenAI integration packages (depending on your LlamaIndex version)")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
