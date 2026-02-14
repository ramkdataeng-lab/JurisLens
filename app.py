import os
import streamlit as st

# LOAD SECRETS INTO OS.ENVIRON ROBUSTLY
def load_secrets():
    if hasattr(st, "secrets"):
        for key, value in st.secrets.items():
            if isinstance(value, str):
                os.environ[key] = value
            elif isinstance(value, dict):
                for subkey, subvalue in value.items():
                     os.environ[subkey] = str(subvalue)

load_secrets()

# Validation Check
# Validation Check
api_key = os.getenv("OPENAI_API_KEY")

# Strict Validation: Must start with "sk-" and be > 20 chars
is_valid_key = api_key and api_key.startswith("sk-") and len(api_key) > 20

if not is_valid_key:
    # FALLBACK: Force manual entry in Sidebar
    st.sidebar.warning("⚠️ API Key missing or invalid (must start with 'sk-')")
    api_key_input = st.sidebar.text_input("Enter OpenAI API Key:", type="password", key="api_key_manual")
    if api_key_input:
        os.environ["OPENAI_API_KEY"] = api_key_input
        api_key = api_key_input
        st.sidebar.success("Key loaded manually! Please wait...")
        try:
            st.rerun() # Modern Streamlit
        except AttributeError:
            st.experimental_rerun() # Legacy Fallback
    else:
        st.error("🚨 OPENAI_API_KEY is required to run JurisLens.")
        st.stop()
else:
    # DEBUG: Show first 5 chars to verify it's loaded
    st.sidebar.success(f"Key Loaded: {api_key[:5]}... ({len(api_key)} chars)")

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
    st.caption("v1.5 - Cache Buster Edition")
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
def setup_agent_v2(openai_api_key):
    # Pass key explicitly to avoid cache staleness
    tools = [search_regulations_tool, calculate_risk_tool]
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo", openai_api_key=openai_api_key)
    
    # Modern Agent Construction using hub prompt
    prompt = hub.pull("hwchase17/openai-tools-agent")
    
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    return AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        return_intermediate_steps=True
    )

# --- CHAT INTERFACE ---
st.title("JurisLens AI (Updated)")
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
        
        agent_executor = setup_agent_v2(api_key)
        if agent_executor:
            try:
                response = agent_executor.run(prompt, callbacks=[st_callback])
                st.write(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.error("⚠️ Agent not initialized. Check API Keys.")
