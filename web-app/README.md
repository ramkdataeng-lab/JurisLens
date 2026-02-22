# 🏛️ JurisLens: Elastic Agent Builder Pro

JurisLens is an autonomous compliance agent designed for the **Elasticsearch Agent Builder Hackathon**. It leverages the latest Elastic-native AI features to navigate complex global financial regulations.

## 🚀 Upgraded Features
- **ELSER v2 Semantic Search**: Upgraded from standard vector search to Elastic's **ELSER v2** (`text_expansion`) for superior semantic understanding of legal texts.
- **ES|QL Audit Engine**: The `RiskCalculator` tool now simulates/executes **ES|QL (Elasticsearch Query Language)** queries for transparent, high-speed transaction history aggregation.
- **Hybrid Search**: Combines ELSER's semantic power with keyword matching for precise citation of legal clauses (e.g., "Section 1010.610").
- **Multi-Step Reasoning**: Built on **LangChain Agents** to orchestrate tool-use across search, risk calculation, and sanctions checking.

## 🛠️ Tech Stack
- **Frontend**: Next.js 15+ (App Router), TailwindCSS, Framer Motion.
- **Backend API**: Next.js Route Handlers.
- **AI Core**: LangChain + OpenAI GPT-4 Turbo.
- **Knowledge Base**: Elasticsearch Cloud.
- **Retrieval**: ELSER v2 + RRF (Reciprocal Rank Fusion) ready.

## 🚦 Getting Started
1. **Clone the repo**: `git clone https://github.com/ramkdataeng-lab/JurisLens`
2. **Setup Env**: Copy `.env.local.example` to `.env.local` and add:
   - `OPENAI_API_KEY`
   - `ELASTIC_CLOUD_ID`
   - `ELASTIC_API_KEY`
3. **Install**: `npm install`
4. **Run**: `npm run dev`

## 🏆 Hackathon Alignment
This project specifically targets the following tracks:
- **Automate messy internal work**: Compliance checks and AML triage.
- **Narrow domain**: Fintech/Legal.
- **Multi-step reasoning**: Agents that plan and verify legal findings.
