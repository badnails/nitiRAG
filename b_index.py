# --- File: build_index.py (using FAISS) ---

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS  # Import FAISS instead of Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from scrape import get_all_data # Import scraping function

# --- Configuration Constants ---
FAISS_INDEX_PATH = "./faiss_index"  # Directory to save the FAISS index
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

def create_and_store_index():
    """Fetches data, processes it, creates embeddings, and stores them in FAISS."""
    print("Starting indexing process...")

    # --- Step 1: Load Data ---
    print("Loading scraped data...")
    scraped_documents = get_all_data()
    if not scraped_documents:
        print("No documents found. Exiting indexing.")
        return

    # --- Step 2: Convert to LangChain Document Format ---
    langchain_docs = []
    for doc_data in scraped_documents:
        doc = Document(
            page_content=doc_data["content"],
            metadata={"source": doc_data["source_url"], "title": doc_data["title"]}
        )
        langchain_docs.append(doc)
    print(f"Loaded {len(langchain_docs)} documents from scraping.")

    # --- Step 3: Chunking Documents ---
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        separators=["\n\n", "\n", ". ", " ", ""]
    )
    chunks = text_splitter.split_documents(langchain_docs)
    print(f"Split {len(langchain_docs)} documents into {len(chunks)} chunks.")

    # --- Step 4: Embedding Model Initialization ---
    print("Loading embedding model...")
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # --- Step 5: Create FAISS Index from documents ---
    # FAISS.from_documents creates the index in memory from the chunks.
    print("Creating FAISS index...")
    vector_store = FAISS.from_documents(chunks, embedding_model)

    # --- Step 6: Save Index to Disk ---
    # Explicitly save the index to the local file system.
    vector_store.save_local(FAISS_INDEX_PATH)
    print(f"FAISS index created and saved successfully at {FAISS_INDEX_PATH}!")

# --- Main execution block ---
if __name__ == "__main__":
    create_and_store_index()