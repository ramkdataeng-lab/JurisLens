
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
    top_local = []  # Initialize to avoid UnboundLocalError
    if "kb_text" in st.session_state and st.session_state.kb_text:
        query_terms = query.lower().split()
        for item in st.session_state.kb_text:
            content = item["content"].lower()
            # Simple keyword matching: count hits
            hits = sum(1 for term in query_terms if term in content and len(term) > 3)
            if hits > 0:
                # Mock score: Normalized to 0-1 range roughly
                score = min(0.99, hits / 10.0) 
                local_results.append((score, item))
        
        # Sort by relevance
        local_results.sort(key=lambda x: x[0], reverse=True)
        # Take top 3
        top_local = local_results[:3]

    # 2. Try Elastic Search
    elastic_results = None
    if os.getenv("ELASTIC_CLOUD_ID"):
        try:
            # Initialize Store
            embeddings = OpenAIEmbeddings()
            vector_store = ElasticsearchStore(
                embedding=embeddings,
                es_cloud_id=os.getenv("ELASTIC_CLOUD_ID"),
                es_api_key=os.getenv("ELASTIC_API_KEY"),
                index_name="jurislens_docs"
            )
            # Use similarity search WITH SCORE
            docs_and_scores = vector_store.similarity_search_with_score(query, k=3)
            
            if docs_and_scores:
                formatted_docs = []
                for doc, score in docs_and_scores:
                    source = doc.metadata.get('source', 'Unknown')
                    page_meta = doc.metadata.get('page', None)
                    
                    citation_part = f"[Source: {source}]"
                    if page_meta is not None:
                        try:
                            # Only add page if it's a valid integer (PDFs usually have 0-indexed pages)
                            p_num = int(page_meta) + 1
                            citation_part = f"[Source: {source} (Page {p_num})]"
                        except:
                            pass
                    
                    # Elastic scores
                    formatted_docs.append(f"{citation_part} [Relevance: {score:.4f}]\n{doc.page_content}")
                elastic_results = "\n\n".join(formatted_docs)
                
        except Exception as e:
            print(f"Elastic Search Failed: {e}")

    # 3. Return Best Available
    if elastic_results:
        return elastic_results
    
    if top_local:
        return "\n\n".join([f"[Source: {item['source']} | Relevance: {score:.2f} (Local Keyword Match)]\n{item['content']}" for score, item in top_local])

    return "No relevant regulations found in Knowledge Base (Elastic + Local Backup). Please ingest documents first."
