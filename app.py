# --- File: app.py (using FAISS) ---

import streamlit as st
import os
from dotenv import load_dotenv

# --- Core LangChain components ---
from langchain_community.vectorstores import FAISS # Import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

# --- Constants ---
FAISS_INDEX_PATH = "./faiss_index" # Path to saved FAISS index
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"
LLM_MODEL_NAME = "gemini-1.5-flash"

# --- RAG Chain Creation Functions ---
def format_docs(docs):
    return "\n\n".join(
        f"Source URL: {doc.metadata['source']}\nContent: {doc.page_content}" for doc in docs
    )

@st.cache_resource
def load_components():
    """Load all necessary components for the RAG chain."""
    embedding_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

    # Load existing FAISS index from disk
    # allow_dangerous_deserialization=True is required for loading local FAISS indexes.
    try:
        vector_store = FAISS.load_local(
            FAISS_INDEX_PATH, 
            embeddings=embedding_model,
            allow_dangerous_deserialization=True 
        )
    except RuntimeError as e:
        st.error(f"Error loading FAISS index: {e}. Did you run build_index.py first?")
        return None, None

    retriever = vector_store.as_retriever(search_kwargs={"k": 3})

    load_dotenv()
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        st.error("GOOGLE_API_KEY not found in environment variables.")
        return None, None

    llm = ChatGoogleGenerativeAI(model=LLM_MODEL_NAME, google_api_key=google_api_key, temperature=0.1)
    return retriever, llm

# ... (The create_rag_chain function and Streamlit UI code remain exactly the same) ...

def create_rag_chain(retriever, llm):
    prompt_template = """
    You are an expert assistant for Bangladesh e-passport services.
    Your task is to answer user questions based ONLY on the following context provided from the official website.

    GUIDELINES:
    - Answer clearly and concisely using the information from the context.
    - If the context does not contain the answer, state clearly: "I could not find information about that in the provided documents."
    - Cite the source URL for the information you provide. Example: "The fee for X is Y (Source: [URL])."
    - Do not make up information or use external knowledge.

    CONTEXT:
    {context}

    QUESTION:
    {question}

    ANSWER:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# --- Streamlit User Interface ---
st.set_page_config(page_title="Bangladesh e-Passport Assistant", layout="wide")
st.title("🇧🇩 Bangladesh e-Passport Information Assistant")
st.markdown("Ask questions about e-passport procedures based on the official website data.")

retriever, llm = load_components()
if retriever and llm:
    rag_chain = create_rag_chain(retriever, llm)
    user_query = st.text_input("Enter your question:", placeholder="e.g., How much is the fee for an urgent passport?")

    if user_query:
        with st.spinner("Searching for information..."):
            # DEBUGGING BLOCK (Optional but recommended)
            st.markdown("---")
            st.subheader("Debug Mode: Retrieved Context")
            retrieved_docs = retriever.invoke(user_query)
            for i, doc in enumerate(retrieved_docs):
                st.write(f"**Retrieved Chunk {i+1} (Source: {doc.metadata.get('source')})**")
                st.info(doc.page_content)
            st.markdown("---")
            
            # Generate final answer
            response = rag_chain.invoke(user_query)
            st.markdown("### Answer")
            st.markdown(response)
else:
    st.warning("RAG components failed to load. Please check configurations.")