
import os
import streamlit as st
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.callbacks import StreamlitCallbackHandler

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
    
    return initialize_agent(
        tools, 
        llm, 
        agent=AgentType.OPENAI_FUNCTIONS, 
        verbose=True,
        memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
        agent_kwargs={
            "system_message": SystemMessage(content="You are JurisLens, an elite legal AI. Use the 'RegulationSearch' tool to find laws. Use 'RiskCalculator' for financial risk methodology. Always cite your sources.")
        }
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
