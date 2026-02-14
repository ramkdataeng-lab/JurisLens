
import os
from langchain_elasticsearch import ElasticsearchStore
from langchain_openai import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool, StructuredTool

ELASTIC_CLOUD_ID = os.getenv("ELASTIC_CLOUD_ID")
ELASTIC_API_KEY = os.getenv("ELASTIC_API_KEY")

def _search_es(query: str) -> str:
    """
    Performs a semantic search on the 'jurislens_docs' index.
    Returns the top 3 closest regulatory chunks.
    """
    try:
        if not ELASTIC_CLOUD_ID:
            return "Error: Elasticsearch not configured."

        vector_store = ElasticsearchStore(
            embedding=OpenAIEmbeddings(),
            es_cloud_id=ELASTIC_CLOUD_ID,
            es_api_key=ELASTIC_API_KEY,
            index_name="jurislens_docs",
            strategy=ElasticsearchStore.ApproxRetrievalStrategy() 
        )
        # Similarity Search
        docs = vector_store.similarity_search(query, k=3)
        return "\n\n".join([f"[Source: {d.metadata.get('source', 'Unknown')}] {d.page_content}" for d in docs])
    except Exception as e:
        return f"Error connecting to Elasticsearch: {e}"

search_regulations_tool = Tool.from_function(
    func=_search_es,
    name="RegulationSearch",
    description="Useful for finding specific laws, statutes, and compliance regulations. Input should be a question or keywords."
)
