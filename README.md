# NITI

Niti project is a Retrieval-Augmented Generation (RAG) system designed to answer user questions about the Bangladesh e-passport application process. Currently, it uses information from the official epassport.gov.bd website to provide accurate, source-cited answers, minimizing the risk of incorrect information or "hallucination" from the language model.

## Features

### Natural Language Questions
Ask questions in plain English about passport procedures, fees, and requirements.

### Grounded Answers
Responses are generated based only on the content scraped from the official e-passport website.

### Source Citations
Every answer includes the source URL from which the information was retrieved, ensuring verifiability.

### Interactive UI
A simple, easy-to-use web interface built with Streamlit.

## Tech Stack
* Language: Python 3.12+
* Core Framework: LangChain
* Web Scraping: Selenium, BeautifulSoup4
* Vector Database: ChromaDB for local storage
* Embeddings: Sentence-Transformers (all-MiniLM-L6-v2)
* LLM: Google Gemini 1.5 Flash (via API)
* Frontend: Streamlit

## Getting Started
Follow these instructions to set up and run the project on your local machine.

### Prerequisites

* **Python 3.10 or higher**: Ensure you have a compatible Python version installed.
* **Git**: You will need Git to clone the repository.
* **Google API Key**: Obtain a free API key with the Gemini API enabled from [Google AI Studio](https://aistudio.google.com/).

*This key is sensitive and should not be shared publicly.*

## Installation

1. **Clone the Repository**

```bash
git clone https://github.com/badnails/nitiRAG.git
cd nitiRAG
```

2. **Create a Virtual Environment**

It's highly recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

3. **Activate the Virtual Environment**

* On **macOS / Linux**:
```bash
source venv/bin/activate
```
* On **Windows**:
```bash
venv\Scripts\activate
```

4. **Install Dependencies**

Install all required packages from the requirements.txt file.

```bash
pip install -r requirements.txt
```

5. **Set Up Your API Key**

Create a new file named `.env` in the root directory of the project.

Add your Google API Key to this file as follows:

```
GOOGLE_API_KEY=YOUR_API_KEY_HERE
```

This file is included in `.gitignore` and will not be uploaded to GitHub.

## Usage

The project has two main steps: building the knowledge base (run once) and running the application.

### 1. Build the Knowledge Base

First, you need to run the script that scrapes the website data, processes it, and builds the local ChromaDB vector index.

```bash
python build_index.py
```

You only need to run this script once to create the FAISS database. If you want to update the knowledge base with new information from the website, you can re-run it.

### 2. Run the Web Application

To start the interactive Streamlit application, run the following command:

```bash
streamlit run app.py
```

This will start a local web server. Open the URL provided in your terminal (usually `http://localhost:8501`) in your web browser to start asking questions.

## How It Works

The system operates in two main phases:

**Indexing Pipeline (Offline):**
Scrape Website → Clean & Chunk Text → Generate Embeddings → Store in ChromaDB Index

**Query Pipeline (Online):**
User Question → Generate Query Embedding → Retrieve Relevant Chunks from ChromaDB → Augment Prompt with Context → Generate Answer with LLM

## Project Files

* `app.py`: The main Streamlit application file containing the UI and RAG chain logic.
* `scrape.py`: The BeautifulSoup-based script for scraping website content.
* `build_index.py`: The script for processing scraped data and creating the FAISS vector index.
* `requirements.txt`: A list of all Python package dependencies.
* `.env`: A file to securely store your Google API key (you must create this).
* `.gitignore`: Specifies files and directories to be ignored by Git.
* `README.md`: This file.