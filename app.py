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
    # Key is valid, proceed silently
    pass

from langchain_openai import ChatOpenAI
from langchain_core.tools import Tool
# Flexible Agent Import for Streamlit Cloud Compatibility
try:
    from langchain.agents import AgentExecutor, create_tool_calling_agent
except ImportError:
    pass

# FALLBACK TO RELIABLE LEGACY AGENT
from langchain.agents import initialize_agent, AgentType
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
    
    # Knowledge Base Section
    with st.expander("📚 Knowledge Base", expanded=True):
        st.markdown("**Upload Regulations**")
        uploaded_files = st.file_uploader("Upload PDF", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
        
        if st.button("Process & Index", type="primary", use_container_width=True):
            if not uploaded_files:
                st.warning("Please upload files first.")
            else:
                import tempfile
                from ingest import ingest_pdf
                
                # Initialize session state for tracking indexed files if not exists
                if "indexed_files" not in st.session_state:
                    st.session_state.indexed_files = set()

                with st.status("Processing Documents...", expanded=True) as status:
                    total_docs = 0
                    for uploaded_file in uploaded_files:
                        st.write(f"📄 Processing: {uploaded_file.name}...")
                        
                        # Save to temp file because PyPDFLoader needs a path
                        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                            tmp_file.write(uploaded_file.getvalue())
                            tmp_path = tmp_file.name
                        
                        try:
                            # Ingest
                            ingest_pdf(tmp_path)
                            total_docs += 1
                            st.session_state.indexed_files.add(uploaded_file.name)
                        except Exception as e:
                            st.error(f"Error processing {uploaded_file.name}: {e}")
                        finally:
                            # Cleanup temp file
                            if os.path.exists(tmp_path):
                                os.remove(tmp_path)
                            
                    status.update(label=f"✅ Indexed {total_docs} Documents!", state="complete", expanded=False)
        
        # Display Indexed Files List
        if "indexed_files" in st.session_state and st.session_state.indexed_files:
            st.markdown("---")
            st.markdown("**🗂️ Indexed Documents:**")
            for filename in st.session_state.indexed_files:
                st.caption(f"✅ {filename}")
    
    st.markdown("---")
    st.info("""
    **⚡ Why Elasticsearch?**
    Unlike standard chatbots limited by context size:
    *   **Scale:** Index **thousands** of PDFs, not just one.
    *   **Precision:** Find exact regulations in milliseconds.
    *   **Privacy:** Data stays in your private vectors.
    """)

    st.markdown("---")
    
    # 2. Controls
    if st.button("🧹 Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()

# --- AGENT SETUP ---
@st.cache_resource
def setup_agent_v2(openai_api_key):
    # Pass key explicitly to avoid cache staleness
    tools = [search_regulations_tool, calculate_risk_tool]
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo", openai_api_key=openai_api_key)
    
    # Use the High-Level "initialize_agent" -> It handles everything automatically
    # This is much more stable on Streamlit Cloud than manual Prompt+AgentExecutor construction
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        max_iterations=5,
        early_stopping_method="generate",
        agent_kwargs={
            "system_message": SystemMessage(content="You are JurisLens, an AI compliance expert. Use provided tools to find regulations and calculate risks. ALWAYS explain your reasoning.")
        }
    )

# --- CHAT INTERFACE ---
st.title("JurisLens AI")
st.markdown("Your autonomous compliance assistant.")

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
        # Cool visualization of the thought process
        with st.status("🤖 AI Processing...", expanded=True) as status:
            st_callback = StreamlitCallbackHandler(st.container())
            agent_executor = setup_agent_v2(api_key)
            
            if agent_executor:
                try:
                    response = agent_executor.run(prompt, callbacks=[st_callback])
                    st.write(response) # Show final answer inside expander
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    status.update(label="✅ Complete!", state="complete", expanded=False)
                except Exception as e:
                    st.error(f"Error: {e}")
                    status.update(label="❌ Error", state="error", expanded=True)
            else:
                st.error("⚠️ Agent not initialized.")
