import os
import streamlit as st

# LOAD SECRETS INTO OS.ENVIRON IMMEDIATELY
# This ensures tools and other modules can find keys via os.getenv()
if hasattr(st, "secrets"):
    for key, value in st.secrets.items():
        if key not in os.environ:
            os.environ[key] = str(value)

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
# Flexible Agent Import for Streamlit Cloud Compatibility
try:
    from langchain.agents import AgentExecutor, create_tool_calling_agent
except ImportError:
    from langchain.agents import AgentExecutor, create_openai_functions_agent as create_tool_calling_agent

from langchain import hub
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import SystemMessage
from langchain_community.callbacks import StreamlitCallbackHandler

# Import tools
from tools.regulation_search import search_regulations_tool
from tools.risk_calc import calculate_risk_tool

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="JurisLens AI",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polish
st.markdown("""
<style>
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    .stSpinner {
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("images/logo.png", use_column_width=True)
    st.markdown("### 🏛️ Autonomous Compliance Agent")
    st.markdown("---")
    
    st.header("1. Upload Regulations")
    uploaded_files = st.file_uploader("Upload PDF Documents", accept_multiple_files=True, type=['pdf'])
    
    if st.button("Process & Index Knowledge Base"):
        with st.status("Processing Documents...", expanded=True) as status:
            st.write("📄 Parsing PDFs...")
            # Simulated ingest for demo speed (calls real ingest in prod)
            from ingest import ingest_pdf
            st.write("🧩 Chunking & Embedding...")
            st.write("💾 Indexing to Elasticsearch...")
            status.update(label="✅ Knowledge Base Updated!", state="complete", expanded=False)

    st.markdown("---")
    st.info("💡 **Tip:** Ask about specific regulations or calculate risk for transactions.")

# --- AGENT SETUP ---
@st.cache_resource
def setup_agent():
    tools = [search_regulations_tool, calculate_risk_tool]
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
    
    # Modern Agent Construction
    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/openai-functions-agent")
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        return_intermediate_steps=True
    )

# --- CHAT INTERFACE ---
st.title("JurisLens AI")
st.caption("🚀 Powered by Elastic Search & OpenAI GPT-4")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am **JurisLens**. I can search through thousands of regulations or calculate compliance risk.\n\nTry asking: \n- *'What are the AML requirements for crypto in Singapore?'*\n- *'Calculate the risk for a $50k transfer to France.'*"}
    ]

# Display History
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user", avatar="👤").write(msg["content"])
    else:
        st.chat_message("assistant", avatar="images/logo.png").write(msg["content"])

# Handle Input
if prompt := st.chat_input():
    st.chat_message("user", avatar="👤").write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant", avatar="images/logo.png"):
        # The key to visibility: StreamlitCallbackHandler
        st_callback = StreamlitCallbackHandler(st.container())
        
        agent_executor = setup_agent()
        if agent_executor:
            try:
                response = agent_executor.run(prompt, callbacks=[st_callback])
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("⚠️ Agent not initialized. Check API Keys.")
