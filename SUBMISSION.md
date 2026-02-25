# JurisLens: The Autonomous Compliance Agent

### **1. Summary**
JurisLens is an autonomous compliance guardian that bridges the gap between static legal rigor and dynamic enterprise state. Unlike passive RAG systems, JurisLens uses **ELSER v2** for deep semantic understanding and **ES|QL** for real-time risk auditing, effectively "enforcing" regulations rather than just reading them.

---

### **2. The Problem**
Global financial institutions face billions in fines because standard AI "hallucinates" laws or lacks access to the real-time "state" of a client's transactions. A chatbot might know the daily transfer limit is $5,000 (static rule), but it doesn't know the client has already sent $4,500 this morning (dynamic state). This **"State-Blindness"** is a multi-billion-dollar liability.

---

### **3. The Solution: JurisLens**
JurisLens is an autonomous agent built on the **Elastic Agent Builder** philosophy. It doesn't just "chat"; it orchestrates a suite of specialized tools to solve the "State-Blindness" problem. Most RAG systems only look at static data (the policy). JurisLens looks at the policy AND the live database simultaneously.

Key features include:
*   **Semantic Law Search:** Powered by **ELSER v2**, it understands the *intent* of complex statutes, such as "Is this client sanctioned?" vs "Can we onboard this client?".
*   **Stateful Risk Auditing:** It generates and executes **ES|QL (Elasticsearch Query Language)** against live transaction indices to check current balances against policy limits.
*   **Multi-Domain Sanctions:** It intelligently switches tools to scan global watchlists for sanctioned entities using Elastic's vector search capabilities.

---

### **4. Technology Stack**
Our foundation is built on the Elastic stack to ensure massive scale and high precision:
*   **Search Engine:** Elasticsearch Cloud (Hybrid Vector + Keyword Search).
*   **ML Model:** ELSER v2 (`text_expansion`) for high-precision legal retrieval without complex training.
*   **Logic Engine:** ES|QL for deterministic, stateful transaction analysis that bridges the gap between AI reasoning and database truth.
*   **AI Core:** LangChain + OpenAI GPT-4 Omni for agentic orchestration.
*   **Frontend:** Next.js 15 (App Router) with a premium glassmorphic UI.

---

### **5. Three Features We Love & Challenges**
1.  **ELSER v2 Precision:** We loved how ELSER handles dense legal PDFs out of the box. It captured nuances in jurisdiction rules that standard keyword search missed entirely.
2.  **ES|QL Tool Use:** The biggest breakthrough was using the AI to write ES|QL. This grounded the AI's "advice" in hard database numbers, preventing hallucinations about credit limits.
3.  **The Challenge:** Syncing real-time streaming AI responses with high-rigor legal verification required careful prompt engineering to ensure the agent waited for all tool results before reaching a "Decision."

---

### **6. Links**
*   **Live App:** [https://jurislens.vercel.app/](https://jurislens.vercel.app/)
*   **GitHub Repo:** [https://github.com/ramkdataeng-lab/JurisLens](https://github.com/ramkdataeng-lab/JurisLens)
*   **Demo Video:** [https://youtu.be/Fe4deVq3YLM](https://youtu.be/Fe4deVq3YLM)

---

### **7. Social Post**
"Just submitted **JurisLens** to the @elastic AI Hackathon! 🚀 It’s an autonomous agent using #Elasticsearch #ELSERv2 and #ESQL to navigate complex financial regs and enforce real-time compliance. #RAG #LangChain #GenAI"
