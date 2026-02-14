# 🏛️ Elastic JurisLens

> **"Seeing through the complexity of compliance."**

**JurisLens** is an AI-powered legal and compliance agent built for the **Elasticsearch Agent Builder Hackathon 2026**.

## 🚀 The Concept
Financial regulations and legal statutes are dense, complex, and constantly changing. **JurisLens** acts as an intelligent compliance officer that:
1.  **Ingests** massive legal documents (PDFs, statutes, internal policies) into an **Elasticsearch Vector Store**.
2.  **Understands** natural language queries like *"Does this new feature violate AML policies in Singapore?"*.
3.  **Reasons** across multiple documents to provide cited, accurate answers using **RAG (Retrieval Augmented Generation)**.

## 🛠️ Tech Stack
*   **Knowledge Base:** Elasticsearch (Vector Search + BM25 Hybrid Search)
*   **AI Engine:** OpenAI GPT-4 / Elastic AI Assistant
*   **Orchestration:** LangChain / Elastic Agent Framework

## 🏗️ Architecture
```mermaid
graph TD
    User[👩‍💻 Compliance Officer] -->|Uploads PDF / Asks Question| UI[💻 Streamlit Web App]
    
    subgraph "JurisLens Agent (LangChain)"
        UI -->|Natural Language| Agent[🤖 Agent Core (GPT-4)]
        
        Agent -->|Decides to Search| ToolSearch[🔍 Regulation Search Tool]
        Agent -->|Decides to Calculate| ToolRisk[DD Risk Calculator Tool]
    end
    
    subgraph "Knowledge Base (Elasticsearch)"
        Ingest[📄 PDF Ingestion] -->|Chunk & Embed| VectorStore[(🗄️ Elastic Vector Store)]
        ToolSearch <-->|Retrieves Context| VectorStore
    end
    
    ToolRisk -->|Returns Risk Score| Agent
    ToolSearch -->|Returns Laws| Agent
    
    Agent -->|Synthesized Answer| UI
```

## 🔮 Roadmap
- [ ] Ingest functionality for PDF/Text documents.
- [ ] Vector Indexing pipeline.
- [ ] Agentic RAG interface.
