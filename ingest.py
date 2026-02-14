
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings

# Connect to ES Cloud (Or Local)
ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def ingest_pdf(pdf_path, index_name="jurislens_docs"):
    """
    Ingests a PDF into Elasticsearch Vector Store.
    """
    if not ELASTIC_CLOUD_ID:
        print("⚠️ No Elastic Cloud ID found. Skipping ingestion.")
        return

    print(f"📄 Loading PDF: {pdf_path}")
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()

    # Split into Chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    print(f"🧩 Split into {len(docs)} chunks. Indexing to '{index_name}'...")
    
    # Store in Elasticsearch
    vector_store = ElasticsearchStore.from_documents(
        docs,
        embedding=OpenAIEmbeddings(),
        es_cloud_id=ELASTIC_CLOUD_ID,
        es_api_key=ELASTIC_API_KEY,
        index_name=index_name,
        strategy=ElasticsearchStore.ApproxRetrievalStrategy() # Uses HNSW
    )
    
    print("✅ Indexing Complete!")
