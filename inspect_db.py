# --- File: inspect_db.py ---

from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# --- Configuration Constants ---
CHROMA_DB_PATH = "./chroma_db"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def inspect_database_contents():
    """Loads the vector store and prints all documents and metadata."""
    
    print("Loading embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    print(f"Loading vector store from: {CHROMA_DB_PATH}")
    try:
        vector_store = Chroma(
            persist_directory=CHROMA_DB_PATH,
            embedding_function=embedding_model
        )
    except Exception as e:
        print(f"Error loading vector store: {e}")
        print("Ensure you have run 'build_index.py' successfully first.")
        return

    # --- Fetch all documents from the collection ---
    # The .get() method retrieves documents. By default, it has limits,
    # but for a small number of chunks (like 4), it should fetch all.
    # We include 'metadatas' and 'documents' to see everything.
    try:
        results = vector_store.get(include=["metadatas", "documents"])
    except Exception as e:
        print(f"Error fetching data from Chroma collection: {e}")
        # This can happen if the collection name used during creation was different.
        # If the default collection name logic fails, direct inspection might be needed.
        return

    all_documents = results.get('documents', [])
    all_metadata = results.get('metadatas', [])

    if not all_documents:
        print("\nNo documents found in the vector store.")
        return

    print(f"\n--- Database Inspection Results ---")
    print(f"Found {len(all_documents)} chunks in the database.\n")

    for i, (content, metadata) in enumerate(zip(all_documents, all_metadata)):
        print(f"--- Chunk {i+1} ---")
        print(f"Source: {metadata.get('source', 'N/A')}")
        print(f"Title: {metadata.get('title', 'N/A')}")
        print("Content Snippet:")
        print(content[:300] + "...") # Print first 300 characters of the chunk
        print("-" * (len(f"--- Chunk {i+1} ---")) + "\n")

# --- Run the inspection ---
if __name__ == "__main__":
    inspect_database_contents()