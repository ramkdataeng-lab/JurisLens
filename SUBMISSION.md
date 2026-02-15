# JurisLens: The Autonomous Compliance Agent

## 1. Description (~400 Words)

**Problem Solved**
Global financial institutions face billions of dollars in fines annually due to non-compliance with Anti-Money Laundering (AML) and Know Your Customer (KYC) regulations. These regulations (like the US Patriot Act, EU’s MiCA, or Singapore’s AML Act) are vast, complex, and constantly changing. Compliance officers spend countless hours manually CTRL+F searching through thousands of PDF pages, often missing critical nuances. Standard chatbots fail here because they hallucinate laws or cannot access private, up-to-the-minute regulatory documents.

**The Solution: JurisLens**
JurisLens is an **Autonomous Compliance Agent** designed to bridge the gap between legal rigor and AI speed. Unlike a passive chatbot, JurisLens is an "Agent" equipped with specialized tools. It can:
1.  **Search & Retrieve:** actively query a secure Knowledge Base of regulations using Semantic Search to find the exact legal clauses relevant to a user's question.
2.  **Calculate Risk:** switch modes to perform deterministic financial risk assessments based on transaction parameters.
3.  **Cite Sources:** provide answers grounded in the actual text of the regulations, reducing liability.

**Features Used & Architecture**
*   **Elasticsearch Vector Store:** The backbone of our Knowledge Base. We use Elastic to store vector embeddings of regulatory PDFs. This allows for semantic retrieval (finding "money laundering rules" even if the text says "illicit financing countermeasures").
*   **LangChain Agents:** We utilize the `OpenAI Functions Agent` architecture. This allows the LLM to "decide" whether to search the database, calculate a number, or just chat, depending on the user intent.
*   **RAG Pipeline:** A complete ingestion pipeline that chunks patents/laws, embeds them using OpenAI models, and indexes them into Elastic Cloud.

**3 Features We Liked & Challenges**
1.  **Elasticsearch Speed:** The retrieval speed for vector search was phenomenal. Even with dense legal texts, Elastic returned relevant chunks in milliseconds, making the chat feel instantaneous.
2.  **Hybrid Tool Use:** We loved how the Agent could seamlessly combine data from a PDF search with a Python-based risk calculator in a single conversation turn. It felt like "Reasoning," not just text prediction.
3.  *(Challenge)*: **Prompt Engineering for Tools.** Getting the agent to consistently call the `RiskCalculator` with the correct JSON schema (e.g., separating "50k" into `50000`) was tricky, but moving to Pydantic-based structured tools solved it.

---

## 2. Demonstration Video
*(Paste your YouTube/Loom link here)*

## 3. Code Repository
https://github.com/ramkdataeng-lab/JurisLens

## 4. Social Post
"Just built JurisLens for the @elastic AI Hackathon! 🚀 It's an autonomous agent that uses #Elasticsearch vector search to navigate complex financial regulations in seconds. Goodbye manual compliance checks! #AI #RAG #LangChain #Python"
