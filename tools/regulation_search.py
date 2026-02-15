
import os
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

@tool
def search_regulations_tool(query: str) -> str:
    """
    Useful for finding specific laws, statutes, and compliance regulations from the knowledge base.
    
    Args:
        query: The search query or question to find relevant regulations for.
    """
    try:
        # Check environment variables inside the function to allow for runtime loading
        if not os.getenv("ELASTIC_CLOUD_ID"):
             # Fallback for demo if no Elastic Cloud configured
            return "Note: Elasticsearch is not configured in this demo environment. Using simulated knowledge base.\n[Source: Simulated] Relevant regulation found: Standard AML procedures require identity verification for transactions over $10k."
            
        vector_store = ElasticsearchStore(
            embedding=OpenAIEmbeddings(),
            es_cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
            es_api_key=os.getenv("ELASTIC_API_KEY"),
            index_name="jurislens_docs",
            strategy=ElasticsearchStore.ApproxRetrievalStrategy() 
        )
        # Similarity Search
        docs = vector_store.similarity_search(query, k=3)
        if not docs:
            return "No relevant regulations found in the knowledge base."
            
        return "\n\n".join([f"[Source: {d.metadata.get('source', 'Unknown')}] {d.page_content}" for d in docs])
    except Exception as e:
        return f"Error connecting to Elasticsearch: {e}"
