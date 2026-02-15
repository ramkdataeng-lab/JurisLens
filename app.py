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
# Custom CSS for polish and branding
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #f8f9fa;
    }
    
    /* Custom Purple Button for 'primary' type */
    div.stButton > button:first-child {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); /* Soft Metallic Purple */
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px -1px rgba(139, 92, 246, 0.3);
    }
    div.stButton > button:first-child:hover {
        background: linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%); /* Slightly darker on hover */
        transform: translateY(-1px);
        box-shadow: 0 6px 8px -1px rgba(124, 58, 237, 0.4);
    }
    div.stButton > button:first-child:active {
        transform: translateY(0px);
    }
    
    /* Chat Bubbles */
    .stChatMessage {
        background-color: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        margin-bottom: 0.5rem;
    }
    
    /* Header Typography */
    h1 { color: #1e293b; font-family: 'Inter', sans-serif;}
    
    /* Hide Deploy Button */
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (MINIMALIST) ---
with st.sidebar:
    st.image("images/logo.png", use_column_width=True)
    st.markdown("### 🏛️ Compliance Agent")
    st.markdown("---")
    
    # Knowledge Base Section
    with st.expander("📚 Knowledge Base", expanded=True):
        uploaded_files = st.file_uploader("Upload Regulations (PDF)", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
        url_input = st.text_input("Or Paste Web Link:", placeholder="https://example.com/regulation")
        
        if st.button("Process & Index", type="primary", use_container_width=True):
            if not uploaded_files and not url_input:
                st.warning("Please upload files or provide a link.")
            else:
                import tempfile
                from ingest import ingest_pdf, ingest_url
                
                # Initialize session state for tracking indexed files if not exists
                if "indexed_files" not in st.session_state:
                    st.session_state.indexed_files = set()

                with st.status("Processing...", expanded=True) as status:
                    total_docs = 0
                    
                    # 1. Process PDFs
                    if uploaded_files:
                        for uploaded_file in uploaded_files:
                            # Save to temp file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                                tmp_file.write(uploaded_file.getvalue())
                                tmp_path = tmp_file.name
                            
                            try:
                                ingest_pdf(tmp_path)
                                total_docs += 1
                                st.session_state.indexed_files.add(uploaded_file.name)
                            except Exception as e:
                                st.error(f"Error PDF: {e}")
                            finally:
                                if os.path.exists(tmp_path):
                                    os.remove(tmp_path)

                    # 2. Process URL
                    if url_input:
                        try:
                            st.write(f"🌐 Crawling: {url_input}...")
                            ingest_url(url_input)
                            total_docs += 1
                            st.session_state.indexed_files.add(url_input)
                        except Exception as e:
                            st.error(f"Error URL: {e}")
                            
                    status.update(label=f"✅ Indexed {total_docs} Items!", state="complete", expanded=False)

    st.markdown("---")
    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        try:
            st.rerun()
        except AttributeError:
            st.experimental_rerun()

# --- AGENT SETUP ---
@st.cache_resource
def setup_agent_v3(openai_api_key):
    # Pass key explicitly to avoid cache staleness
    tools = [search_regulations_tool, calculate_risk_tool]
    llm = ChatOpenAI(temperature=0, model="gpt-4-turbo", openai_api_key=openai_api_key)
    
    # Use the High-Level "initialize_agent" -> It handles everything automatically
    return initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        max_iterations=5,
        early_stopping_method="generate",
        agent_kwargs={
            "system_message": SystemMessage(content="You are JurisLens, an AI compliance expert. Use provided tools. For 'RegulationSearch', provide ONLY the 'query' string.")
        }
    )

# Helper to clean up response and add visual cues
def enrich_response(text):
    if not text: return text
    lower_text = text.lower()
    
    # Check for High Risk keywords
    if "high risk" in lower_text or "risk level is high" in lower_text or "risk level: high" in lower_text or "critical risk" in lower_text or "considered high" in lower_text:
        return f"### 🔴 📈 HIGH RISK ALERT\n\n{text}"
    
    # Check for Medium Risk keywords
    elif "medium risk" in lower_text or "risk level is medium" in lower_text or "risk level: medium" in lower_text or "moderate risk" in lower_text:
        return f"### 🟠 ⚠️ MEDIUM RISK WARNING\n\n{text}"
    
    # Check for Low Risk keywords
    elif "low risk" in lower_text or "risk level is low" in lower_text or "risk level: low" in lower_text or "minimal risk" in lower_text:
        return f"### 🟢 📉 LOW RISK ASSESSMENT\n\n{text}"
        
    return text

# --- MAIN LAYOUT (2 COLUMNS) ---
# Create a 2-column layout: [Chat Area (75%), Info Panel (25%)]
chat_col, info_col = st.columns([0.75, 0.25], gap="large")

with chat_col:
    # Fancy Header
    st.markdown("<h1>⚖️ JurisLens AI</h1>", unsafe_allow_html=True)
    st.markdown("#### *Navigate Global Financial Regulations with Autonomous Precision.*")
    
    # Tech Badges
    st.caption("🚀 Powered by **Elasticsearch RAG** | **OpenAI GPT-4** | **LangChain Agents**")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "Hello! I am **JurisLens**. I can search through thousands of regulations or calculate compliance risk.\n\nTry asking: \n- *'What are the AML requirements for crypto in Singapore?'*\n- *'Calculate the risk for a $50k transfer to France.'*"}
        ]

    # Handle Input - Pinned to bottom by default
    if prompt := st.chat_input("Ask a compliance question..."):
        # Add user message to state
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # We need to process immediately
        with st.chat_message("user", avatar="👤"):
             st.write(prompt)

        with st.chat_message("assistant", avatar="images/logo.png"):
             # Cool visualization of the thought process
            with st.status("🤖 AI Processing...", expanded=True) as status:
                st_callback = StreamlitCallbackHandler(st.container())
                agent_executor = setup_agent_v3(api_key)
                
                if agent_executor:
                    try:
                        response = agent_executor.run(prompt, callbacks=[st_callback])
                        status.update(label="✅ Complete!", state="complete", expanded=False)
                    except Exception as e:
                        st.error(f"Error: {e}")
                        status.update(label="❌ Error", state="error", expanded=True)
                        response = None
                else:
                    st.error("⚠️ Agent not initialized.")
                    response = None
            
            # Show final answer
            if response:
                final_text = enrich_response(response)
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Feedback for current answer
                col1, col2, col3 = st.columns([1, 1, 8])
                with col1: st.button("👍", key="curr_up", help="Helpful")
                with col2: st.button("👎", key="curr_down", help="Not Helpful")

    st.markdown("### 💬 Conversation History")
    
    # Logic: If we just added a new Q&A pair (prompt is True), 
    # we don't want to show it in history yet (because it's shown above).
    # So we slice the list to exclude the last 2 messages.
    # Otherwise, show everything.
    
    all_messages = st.session_state.messages
    history_messages = all_messages[:-2] if prompt and len(all_messages) >= 2 else all_messages
    
    # Reverse iterate for history
    for i in range(len(history_messages) - 1, -1, -1):
        msg = history_messages[i]
        
        if msg["role"] == "user":
            user_msg = msg
            ai_msg = None
            
            # Find pairing in the sliced list
            if i + 1 < len(history_messages) and history_messages[i+1]["role"] == "assistant":
                 ai_msg = history_messages[i+1]
            
            with st.container():
                st.chat_message("user", avatar="👤").write(user_msg["content"])
                if ai_msg:
                    with st.chat_message("assistant", avatar="images/logo.png"):
                        # Enrich and Display
                        final_text = enrich_response(ai_msg["content"])
                        st.markdown(final_text)
                        
                        # Feedback Buttons (Small)
                        col1, col2, col3 = st.columns([1, 1, 8])
                        with col1:
                            st.button("👍", key=f"up_{i}", help="Helpful")
                        with col2:
                            st.button("👎", key=f"down_{i}", help="Not Helpful")
                            
                st.markdown("---")

    # Show initial greeting if it exists and wasn't part of the loop (e.g. index 0)
    if history_messages and history_messages[0]["role"] == "assistant":
         st.chat_message("assistant", avatar="images/logo.png").write(history_messages[0]["content"])

# --- RIGHT INFO PANEL ---
with info_col:
    st.markdown("### ⚡ Engine")
    st.info("""
    *   **Search:** Elasticsearch Vector Store
    *   **Model:** GPT-4 Turbo
    *   **Framework:** LangChain Agents
    """)
    
    st.markdown("### 🏆 Why Elastic?")
    st.info("""
    **⚡ Powered by Elasticsearch RAG**
    Unlike standard chatbots limited by context size:
    
    *   **Scale:** Index **thousands** of PDFs, not just one.
    *   **Precision:** Find exact regulations in milliseconds.
    *   **Privacy:** Data stays in your private vectors.
    """)
    
    # Display Indexed Files List Here
    if "indexed_files" in st.session_state and st.session_state.indexed_files:
        st.markdown("---")
        st.markdown("### 🗂️ Active Docs")
        for filename in st.session_state.indexed_files:
            st.success(f"📄 {filename}")
