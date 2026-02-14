
import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool, StructuredTool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage

# Import our custom Elasticsearch tool
from tools.regulation_search import search_regulations_tool
from tools.risk_calc import calculate_risk_tool

# Page Config
st.set_page_config(page_title="JurisLens 🏛️", layout="wide")

st.title("🏛️ JurisLens: Autonomous Compliance Agent")
st.markdown("> **Navigate Regulations with Precision.** Powered by Elastic AI Search & OpenAI.")

# --- SIDEBAR: Configuration & Setup ---
with st.sidebar:
    st.header("Upload Regulations")
    uploaded_files = st.file_uploader("Upload PDF Documents", accept_multiple_files=True, type=['pdf'])
    
    if st.button("Process & Index"):
        st.info("Indexing logic triggered... (See ingest.py)")
        from ingest import ingest_pdf
        # Note: In a real app, save file to temp and pass path
        st.success("Indexing Simulation Complete!")

# --- AGENT SETUP ---
@st.cache_resource
def setup_agent():
    # 1. Define Tools
    tools = [
        search_regulations_tool,  # RAG Tool (Elasticsearch)
        calculate_risk_tool       # Python Logic Tool
    ]

    # 2. Initialize LLM (GPT-4 Turbo for reasoning)
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))

    # 3. Create Agent (OpenAI Functions Agent is best for tool usage)
    agent = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.OPENAI_FUNCTIONS, 
        verbose=True,
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
        agent_kwargs={
            "system_message": SystemMessage(content="You are JurisLens, an expert compliance officer. You use tools to search regulations and calculate risk. Always cite your sources from the search tool.")
        }
    )
    return agent

try:
    if os.getenv("OPENAI_API_KEY"):
        agent_executor = setup_agent()
    else:
        st.error("⚠️ OpenAI API Key missing. Agent cannot start.")
        agent_executor = None
except Exception as e:
    st.error(f"⚠️ Agent Error: {e}")
    agent_executor = None


# --- CHAT INTERFACE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle User Input
prompt = st.chat_input("Ask: 'Does this crypto transaction violate AML rules?'")

if prompt:
    # 1. User Message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
    # 2. Agent Response
    with st.chat_message("assistant"):
        if agent_executor:
            with st.spinner("🤖 JurisLens is thinking & searching..."):
                try:
                    response = agent_executor.run(prompt)
                    st.markdown(response)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                     st.error(f"Error: {e}")
        else:
             st.markdown("⚠️ Agent not initialized.")
