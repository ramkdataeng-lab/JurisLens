# 🎬 JurisLens: Professional Demo Recording Guide

This guide details exactly how to record your 3-minute hackathon demo. We have synchronized the UI actions with the **12 Audio Segments** generated in the `voiceovers/` folder.

---

## 🛠️ Pre-Recording Checklist
1. **Reset State**: Clear your Elasticsearch index if needed, or ensure the files are ready to be uploaded fresh.
2. **Open Documents**: Have the `goliath_bank_internal_policy.pdf` open in a separate window to show it briefly.
3. **Environment**: Use the **Live Vercel App** at `https://jurislens.vercel.app/`.
4. **Resolution**: Record in **1080p (1920x1080)** for maximum clarity.

---

## 📽️ Scene-by-Scene Director's Cut

### Phase 1: The Hook (0:00 - 0:40)
*   **Audio**: `01_Intro`, `02_TheProblem`
*   **Visual**: 
    *   Start on the JurisLens home screen.
    *   Briefly show a PDF of banking regulations (dense text).
    *   **Action**: Type into JurisLens: *"My client wants to send $4,000 to Zylaria. Is this allowed?"*
    *   **Action**: Switch to a standard ChatGPT/Grok tab. Show it saying "Yes, the limit is $5,000. It's safe." (Or just point to your previous chat history).

### Phase 2: The Solution (0:40 - 1:10)
*   **Audio**: `03_TheBlindSpot`, `04_Solution`
*   **Visual**:
    *   Zoom in on the **"Elastic Agent Builder Pro"** badge in the sidebar.
    *   Transition back to JurisLens. Show the "Powered by ELSER v2" text.
    *   **Action**: Hover over the sidebar sections to show the "Knowledge Base" and "Engine" details.

### Phase 3: The Demo - Ingest (1:10 - 1:30)
*   **Audio**: `05_Demo_Ingest`
*   **Visual**:
    *   **Action**: Select `goliath_bank_internal_policy.pdf`.
    *   **Action**: Click **"⚡ Process & Index"**. 
    *   Wait for the "✅ Indexed!" success message. 

### Phase 4: The Demo - Reasoning (1:30 - 2:00)
*   **Audio**: `06_Demo_AskRule`, `07_Demo_AskAction`
*   **Visual**:
    *   **Action**: Type *"What is the transfer limit for Zylaria under Project Chimera?"*
    *   **Result**: Show the response with the citation: `[Source: Policy.pdf (Page 5)]`.
    *   **Action**: NOW, type the killer question: *"My client wants to send $4,000 to Zylaria. Is this allowed?"*

### Phase 5: The "Wow Factor" - ES|QL Audit (2:00 - 2:25)
*   **Audio**: `08_Demo_Result`
*   **Visual**:
    *   **CRITICAL**: Zoom in on the response as it appears.
    *   Highlight the **"🔴 HIGH RISK ALERT"** and the text: **"Audit Query: [FROM financial-transactions-*...]"**.
    *   Scroll down to show the detailed reasoning: "Blocked. Total exposure $6,500 exceeds $5,000 limit."

### Phase 6: Orchestration (2:25 - 2:45)
*   **Audio**: `09_Scenario2_Sanctions`, `10_Scenario2_Result`
*   **Visual**: 
    *   **Action**: Use the quick-prompt button: *"Can we onboard Ivan Drago?"*.
    *   **Visual**: Show the "🕵️‍♀️ Scanning Sanctions..." status.
    *   **Result**: Show the "🚨 MATCH FOUND" response with the "Action: IMMEDIATE FREEZE" text.

### Phase 7: Tech Stack & Closing (2:45 - 3:00)
*   **Audio**: `11_Closing`, `12_Adoption`
*   **Visual**:
    *   Open the **"🛠️ Architecture"** modal. Scroll through the diagram showing ELSER v2 and the Agent loop.
    *   End with a shot of the **Citations** window showing the semantic relevance score.
    *   Fade out on the logo.

---

## 🎤 Tips for High-Quality Recording
1. **Screen Recording**: Use **OBS Studio** or **Loom (Desktop App)** for high bitrate.
2. **Window Capture**: Don't record your whole desktop. Capture JUST the browser window.
3. **Cursor**: Turn off "Cursor Highlight" unless you are moving slow and deliberate.
4. **Post-Processing**: Use **CapCut** or **iMovie** to drop the audio files (`voiceovers/*.mp3`) onto your video track. 
    *   Apply a "Zoom" effect when you want to show the ES|QL query or the "High Risk" alert.
    *   Add background music at **-20dB** (very quiet) to make it feel premium. Use a "Modern Corporate" or "Cyber-Tech" track.

---

## 🏆 Key Keywords to Mention in Devpost Text
*   "Context-Driven Agents"
*   "Zero-Hallucination via Hybrid Search"
*   "Real-time Enterprise State Enforcement"
*   "Multi-Tool Orchestration"
