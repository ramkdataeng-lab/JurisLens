# 🎥 JurisLens: The 3-Minute Video Pitch Script

**Target Audience:** Hackathon Judges & Enterprise Compliance Officers
**Core Message:** "Generative AI reads rules. Agentic AI *enforces* them. JurisLens bridges the gap between static policy and live enterprise state using Elasticsearch."

---

## ⏱️ 0:00 - 0:40 | The Problem: "The Blind Spot of GenAI"
**(Visual: Split screen. Left: ChatGPT/Grok interface. Right: A busy bank trading floor or database icon.)**

**You:** "We all know LLMs are amazing at reading documents. I can feed 50 pages of banking regulations into Grok, asking *'Is a $4,000 transfer to Zylaria allowed?'*, and it will say **YES**."

**(Visual: Show Grok's response: "Yes, the limit is $5,000. $4,000 is safe.")**

**You:** "Why? Because the rulebook says the limit is $5,000. But Grok is **blind**. It doesn't know that this specific client *already wire-transferred $2,500 this morning*."

**You:** "In the real world, compliance isn't just about reading rules. It's about knowing the **State of the Bank**. And that is where generic LLMs fail catastrophically."

---

## ⏱️ 0:40 - 1:10 | The Solution: JurisLens
**(Visual: JurisLens Logo animating. "Powered by Elasticsearch" badge glowing.)**

**You:** "Introducing **JurisLens**: An Autonomous Compliance Agent that doesn't just read—it **thinks, searches, and checks**."

**You:** "Powered by **Elasticsearch**, JurisLens isn't limited to a context window. It indexes **millions** of internal documents using **Hybrid Search**—combining Vector precision with Keyword exactness to find the one clause that matters in a sea of regulations."

**(Visual: Show the "Hybrid Search" indicator in the sidebar and the "Knowledge Base" loaded with chunks.)**

---

## ⏱️ 1:10 - 2:20 | The Killer Demo: "Project CHIMERA"
**(Visual: Screen recording of JurisLens Interface.)**

**You:** "Let's see the difference. Here is a confidential internal policy for 'Goliath Bank'. It has a strict rule for 'Project Chimera': transfers to 'Zylaria' are capped at **$5,000**."

**(Visual: Briefly show the PDF uploaded to JurisLens.)**

**You:** "I ask JurisLens the same question: *'My client wants to send $4,000 to Zylaria. Is this allowed?'*"

**(Visual: JurisLens processing. Sidebar shows: "🔌 Connecting to Core Banking Ledger... Found prior transaction: $2,500".)**

**You:** "Watch the sidebar. JurisLens retrieves the Policy PDF from Elasticsearch, BUT it also **connects to our Internal Risk Database**."

**(Visual: The Response appears in Green/Red code block.)**

**You:** "Boom. **DENIED.** JurisLens caught what Grok missed. It says: *'Blocked. Client already sent $2,500 today. Total exposure $6,500 exceeds the daily limit.'*"

**You:** "This logic didn't exist in the prompt. The Agent **synthesized** the static rule from the PDF with the dynamic state from the Ledger. That is the power of Agentic AI."

---

## ⏱️ 2:20 - 2:45 | Scenario 2: Universal Compliance Orchestration
**(Visual: User typing: "Can we onboard Ivan Drago as a new client?")**

**You:** "But JurisLens isn't just about money. It's a universal compliance orchestrator. Watch as it detects a different intent—onboarding a person."

**(Visual: Sidebar shows: "🕵️‍♀️ Scanning Sanctions Databases...")**

**You:** "It intelligently switches tools, scanning global sanctions lists in real-time. Grok might tell you Ivan Drago is a boxer; JurisLens tells you he's on the OFAC SDN List and blocks the onboarding."

---

## ⏱️ 2:45 - 3:30 | Tech Stack & Closing
**(Visual: Architecture Diagram slides in. Elasticsearch Logo + LangChain Logo + OpenAI Logo.)**

**You:** "Under the hood, we use **Elasticsearch** as our retrieval backbone because financial compliance requires **zero hallucination**. If a regulation mentions 'Article 1010.610', we need *that exact document*, not a fuzzy match. Elastic's Hybrid Search guarantees that precision."

**(Visual: Show the "Citations" with Page Numbers: "[Source: Policy.pdf (Page 2)]")**

**You:** "We also provide exact citations—down to the page number—for every claim, creating a perfect audit trail."

**You:** "Don't just chat with your data. **Enforce it.** This is JurisLens."

**(Visual: Fade to Black. "JurisLens. Powered by Elasticsearch.")**
