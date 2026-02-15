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
from tools.sanctions import check_sanctions_tool

from langchain.callbacks.base import BaseCallbackHandler
import time

# Custom Handler for user-friendly "Scanning" visuals
class FriendlyCallbackHandler(BaseCallbackHandler):
    def __init__(self, status_placeholder, progress_bar):
        self.status = status_placeholder
        self.progress = progress_bar
        self.step = 30 # Start at 30%
        
    def on_tool_start(self, serialized, input_str, **kwargs):
        tool_name = serialized.get("name")
        self.step += 10
        if self.step > 90: self.step = 90
        self.progress.progress(self.step)
        
        if tool_name == "search_regulations_tool":
            self.status.info("🔍 **Scanning Knowledge Base...**")
        elif tool_name == "calculate_risk_tool":
            self.status.warning("🧮 **Calculating Compliance Risk...**")
        elif tool_name == "check_sanctions_tool":
            self.status.error("🕵️‍♀️ **Scanning Sanctions Databases...**")
            
    def on_tool_end(self, output, **kwargs):
        self.step += 10
        if self.step > 95: self.step = 95
        self.progress.progress(self.step)
        
        output_str = str(output)
        if "Daily Aggregate Limit Exceeded" in output_str:
             self.status.error("❌ **LEDGER CHECK FAILED:** Daily Limit Exceeded!")
        elif "simulated" in output_str.lower() or "source" in output_str.lower():
             self.status.success("✅ **Relevant Documents Found.** Analysis in progress...")
        else:
             self.status.info("🤔 **Analyzing Findings...**")

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
    
    /* Ultra-Compact Sidebar Elements */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.2rem !important;
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem !important;
    }
    
    /* Shrink File Uploader Logic */
    [data-testid="stFileUploader"] {
        padding-top: 0rem !important;
        padding-bottom: 0.5rem !important;
    }
    [data-testid="stFileUploader"] section {
        padding: 0.5rem !important;
        min-height: 0px !important;
    }
    [data-testid="stFileUploader"] label {
        font-size: 0.8rem !important;
        margin-bottom: 0rem !important;
    }
    
    /* Compact Text Input */
    [data-testid="stTextInput"] {
        padding-top: 0rem !important;
    }
    [data-testid="stTextInput"] label {
        font-size: 0.8rem !important;
        margin-bottom: 0rem !important;
    }
    
    /* Header Typography */
    h1 { color: #1e293b; font-family: 'Inter', sans-serif;}
    
    /* Compact Sidebar */
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.5rem !important;
        padding-top: 0rem !important;
    }
    section[data-testid="stSidebar"] > div {
        padding-top: 0rem !important;
    }
    
    /* Hide Deploy Button */
    .stDeployButton {display:none;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR (MINIMALIST) ---
with st.sidebar:
    # Small logo to save space
    st.image("images/logo.png", width=280)
    st.markdown("### ⚡ Elastic RAG  \n<span style='font-size:0.8em;'>🔍 **Mode:** Hybrid (Vector + Keyword)</span>", unsafe_allow_html=True)
    
    # Knowledge Base Section
    with st.expander("📚 Knowledge Base", expanded=True):
        # Stats
        kb_count = len(st.session_state.get("kb_text", []))
        if kb_count > 0:
            st.success(f"✅ KB: {kb_count} Chunks")
        else:
            st.caption("ℹ️ Knowledge Base Empty")

        uploaded_files = st.file_uploader("Upload Regulations (PDF)", type=["pdf"], accept_multiple_files=True, label_visibility="collapsed")
        # Pre-filled placeholder with a real eCFR regulation link for easier demo
        url_input = st.text_input("Or Paste Web Link:", placeholder="https://www.ecfr.gov/current/title-31/part-1010/section-1010.610")
        
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
                            
                    if total_docs > 0:
                        status.update(label=f"✅ Indexed {total_docs} Items!", state="complete", expanded=False)
                    else:
                        status.update(label="❌ Ingestion Failed", state="error", expanded=True)

    if st.button("🧹 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        try:
            st.rerun()
        except AttributeError:
             # Fallback for older streamlit
             pass

# --- AGENT SETUP ---
def setup_agent_v3(openai_api_key):
    # Pass key explicitly to avoid cache staleness
    tools = [search_regulations_tool, calculate_risk_tool, check_sanctions_tool]
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
            "system_message": SystemMessage(content="""You are JurisLens, an AI compliance expert. 
            
            1. Use 'RegulationSearch' to find laws. Provide comprehensive, verbose explanations citing specific articles/sections. 
            2. ALWAYS cite the source document name (e.g., '[Source: Singapore_AML_Act.pdf]') for every claim.
            3. Use 'RiskCalculator' for risk assessment and live ledger checks.
            4. Use 'SanctionsChecker' to verify if individuals or entities are on blacklists or sanctioned watchlists.
            """)
        }
    )

# Helper to clean up response and add visual cues
def enrich_response(text):
    if not text: return text
    lower_text = text.lower()
    
    # Check for High Risk keywords
    if "high risk" in lower_text or "risk level is high" in lower_text or "risk level: high" in lower_text or "critical risk" in lower_text or "considered high" in lower_text:
        return f"**🔴 📈 HIGH RISK ALERT**\n\n{text}"
    
    # Check for Medium Risk keywords
    elif "medium risk" in lower_text or "risk level is medium" in lower_text or "risk level: medium" in lower_text or "moderate risk" in lower_text:
        return f"**🟠 ⚠️ MEDIUM RISK WARNING**\n\n{text}"
    
    # Check for Low Risk keywords
    elif "low risk" in lower_text or "risk level is low" in lower_text or "risk level: low" in lower_text or "minimal risk" in lower_text:
        return f"**🟢 📉 LOW RISK ASSESSMENT**\n\n{text}"
        
    return text

# --- MAIN LAYOUT (2 COLUMNS) ---
# Create a 2-column layout: [Chat Area (75%), Info Panel (25%)]
chat_col, info_col = st.columns([0.75, 0.25], gap="large")

with chat_col:
    # Fancy Header
    st.markdown("<h1>⚖️ JurisLens AI</h1>", unsafe_allow_html=True)
    
    # EMPHASIZE ELASTIC SEARCH
    st.info("⚡ **Powered by Elasticsearch:** Scalable to **Millions** of documents using **Hybrid Search** (Vector + Keyword) for unmatched precision.")
    
    st.markdown("#### *Navigate Global Financial Regulations with Autonomous Precision.*")
    st.markdown("---")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": """Hello! I am **JurisLens**. I can search through thousands of regulations or calculate compliance risk.

**🚀 Try this live demo:**
1. Paste this URL in the sidebar: `https://www.ecfr.gov/current/title-31/part-1010/section-1010.610`
2. Click **Process & Index**.
3. Ask: *'What are the enhanced due diligence requirements for foreign correspondent accounts?'*
"""}
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
            status_viz = st.empty()
            progress_bar = st.progress(0)
             
            # Initial status
            status_viz.info("🤖 **AI Agent Active.** Analyzing request...")
             
            # Simulate a "Scan" effect
            for i in range(1, 30):
                time.sleep(0.01)
                progress_bar.progress(i)
             
            # Use our custom handler defined at top of file
            my_callback = FriendlyCallbackHandler(status_viz, progress_bar)
             
            agent_executor = setup_agent_v3(api_key)
            response = None
                
            if agent_executor:
                try:
                    response = agent_executor.run(prompt, callbacks=[my_callback])
                    # Clear visuals on done
                    status_viz.empty()
                    progress_bar.empty()
                except Exception as e:
                    st.error(f"Error: {e}")
                    response = None

            
            # Show final answer
            if response:
                final_text = enrich_response(response)
                st.markdown(final_text)
                st.session_state.messages.append({"role": "assistant", "content": response})
                
                # Feedback for current answer
                col_spacer, col_up, col_down = st.columns([0.85, 0.08, 0.07])
                with col_up: st.button("👍", key="curr_up", help="Helpful")
                with col_down: st.button("👎", key="curr_down", help="Not Helpful")

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
                        
                        # Feedback Buttons (Right Aligned)
                        # We use a huge spacer to push them right
                        c_space, c_up, c_down = st.columns([0.85, 0.08, 0.07])
                        with c_up:
                            st.button("👍", key=f"up_{i}", help="Helpful")
                        with c_down:
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

# --- FOOTER ---
    # --- FOOTER (In Info Panel) ---
    st.markdown("---")
    st.caption("© 2026 JurisLens Inc. | **Privacy Policy**")
    
# --- HELPER: Architecture Modal (Robust) ---
def show_architecture_content():
    import base64
    
    # Read Image and Encode
    try:
        with open("Arc_diagram/architecture.png", "rb") as f:
            img_bytes = f.read()
        encoded = base64.b64encode(img_bytes).decode()
        
        # Display with CSS precision - Reduced height to ensure legend visibility
        st.markdown(f"""
        <div style="display: flex; justify-content: center;">
            <img src="data:image/png;base64,{encoded}" 
                 style="max-width: 100%; max-height: 65vh; object-fit: contain; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        </div>
        """, unsafe_allow_html=True)
        
    except FileNotFoundError:
        st.error("Architecture diagram not found.")
    
    # Tech Stack Legend
    st.markdown("""
    <div style="text-align: center; margin-top: 10px; padding: 8px; background-color: #f0f2f6; border-radius: 10px;">
        <p style="margin:0; font-weight: bold; color: #31333F; font-size: 0.9em;">🚀 &nbsp; BUILT WITH &nbsp; 🚀</p>
        <p style="margin:5px 0 0 0; font-size: 0.8em;">
            <span style="color:#0077cc;"><b>Streamlit</b></span> (UI) &nbsp;•&nbsp;
            <span style="color:#F5A623;"><b>Elasticsearch</b></span> (Vector Store) &nbsp;•&nbsp;
            <span style="color:#00A67E;"><b>LangChain</b></span> (Orchestration) &nbsp;•&nbsp;
            <span style="color:#7D55C7;"><b>GPT-4</b></span> (Reasoning)
        </p>
    </div>
    """, unsafe_allow_html=True)

# Check which dialog version is available
if hasattr(st, "dialog"):
    show_architecture = st.dialog("JurisLens System Architecture", width="large")(show_architecture_content)
elif hasattr(st, "experimental_dialog"):
    show_architecture = st.experimental_dialog("JurisLens System Architecture", width="large")(show_architecture_content)
else:
    # Fallback for older Streamlit versions (just show in expander)
    def show_architecture():
        with st.expander("JurisLens System Architecture", expanded=True):
            show_architecture_content()

# Call the button inside the layout
with info_col:
    st.markdown("---")
    if st.button("🛠️ Architecture", use_container_width=True):
        show_architecture()
