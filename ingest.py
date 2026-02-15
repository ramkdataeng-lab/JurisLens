
import os
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings

# Connect to ES Cloud (Or Local)
ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ingest_pdf(pdf_path, index_name="jurislens_docs"):
    """
    Ingests a PDF into Elasticsearch Vector Store (and Local Backup).
    """
    print(f"📄 Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    _split_and_index(documents, index_name)

def ingest_url(url, index_name="jurislens_docs"):
    """
    Ingests a Web Page into Elasticsearch Vector Store (and Local Backup).
    """
    print(f"🌐 Loading URL: {url}")
    try:
        # Use valid User-Agent to avoid 403 blocks
        loader = WebBaseLoader(
            url,
            header_template={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
        )
        documents = loader.load()
    except Exception as e:
        raise ValueError(f"Failed to load URL: {e}")
    
    _split_and_index(documents, index_name)

import streamlit as st

def _split_and_index(documents, index_name):
    # Split into Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    if not docs:
         print("⚠️ No content found to index.")
         return

    # --- BACKUP: Store in Session State for Demo ---
    if "kb_text" not in st.session_state:
        st.session_state.kb_text = []
    
    for d in docs:
        st.session_state.kb_text.append({
            "source": d.metadata.get("source", "Unknown"),
            "content": d.page_content
        })
    print(f"💾 Stored {len(docs)} chunks in local backup memory.")
    # -----------------------------------------------

    print(f"🧩 Split into {len(docs)} chunks. Indexing to '{index_name}'...")
    
    # Store in Elasticsearch (if configured)
    if os.getenv("ELASTIC_CLOUD_ID"):
        try:
            vector_store = ElasticsearchStore.from_documents(
                docs,
                embedding=OpenAIEmbeddings(),
                es_cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
                es_api_key=os.getenv("ELASTIC_API_KEY"),
                index_name=index_name,
                strategy=ElasticsearchStore.ApproxRetrievalStrategy() # Uses HNSW
            )
            print("✅ Indexing Complete!")
        except Exception as e:
            print(f"⚠️ Elastic Indexing failed (using local backup): {e}")
    else:
        print("⚠️ Elastic not configured. Using local backup only.")
