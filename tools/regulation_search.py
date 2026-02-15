
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
    # Access session state for local backup
    import streamlit as st
    
    # 1. Try Local Search if Elastic is missing OR as a fallback
    local_results = []
    if "kb_text" in st.session_state and st.session_state.kb_text:
        query_terms = query.lower().split()
        for item in st.session_state.kb_text:
            content = item["content"].lower()
            # Simple keyword matching: count hits
            score = sum(1 for term in query_terms if term in content and len(term) > 3)
            if score > 0:
                local_results.append((score, item))
        # Sort by relevance
        local_results.sort(key=lambda x: x[0], reverse=True)
        local_results = [x[1] for x in local_results[:3]]

    # 2. Try Elastic Search
    elastic_results = None
    if os.getenv("ELASTIC_CLOUD_ID"):
        try:
            vector_store = ElasticsearchStore(
                embedding=OpenAIEmbeddings(),
                es_cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
                es_api_key=os.getenv("ELASTIC_API_KEY"),
                index_name="jurislens_docs",
                strategy=ElasticsearchStore.ApproxRetrievalStrategy() 
            )
            docs = vector_store.similarity_search(query, k=3)
            if docs:
                elastic_results = "\n\n".join([f"[Source: {d.metadata.get('source', 'Unknown')}]\n{d.page_content}" for d in docs])
        except Exception as e:
            print(f"Elastic Search Failed: {e}")

    # 3. Return Best Available
    if elastic_results:
        return elastic_results
    
    if local_results:
        return "\n\n".join([f"[Source: {item['source']}]\n{item['content']}" for item in local_results])

    return "No relevant regulations found in Knowledge Base (Elastic + Local Backup). Please ingest documents first."
