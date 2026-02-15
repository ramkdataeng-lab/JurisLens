
import asyncio
import edge_tts
import os

# Select Voice: 
# "en-US-ChristopherNeural" (Male, Professional)
# "en-US-JennyNeural" (Female, Clear)
VOICE = "en-US-ChristopherNeural"
OUTPUT_DIR = "voiceovers"

SCRIPT = {
    "01_Intro": "Web search engines are great at reading, but terrible at enforcing. Meet JurisLens: The first Autonomous Compliance Agent that bridges the gap between static policy documents and live enterprise data.",
    
    "02_TheProblem": "We all know LLMs can read. I can feed a 50-page banking regulation PDF into a standard chatbot and ask if a $4,000 transfer is allowed. It will read the rule limit of $5,000 and say YES. But in the real world, compliance isn't just about reading rules. It's about knowing the state of the bank.",
    
    "03_TheBlindSpot": "The chatbot is blind. It doesn't know that this specific client already transferred $2,500 this morning. It approves a transaction that actually violates the daily aggregate limit.",
    
    "04_Solution": "Enter JurisLens. An Autonomous Agent built on the Elastic Stack. It uses Hybrid Search—combining vector semantic understanding with keyword precision—to find the exact regulation you need.",
    
    "05_Demo_Ingest": "Watch this. We ingest a confidential internal policy PDF. JurisLens indexes it instantly into Elasticsearch for real-time retrieval.",
    
    "06_Demo_AskRule": "First, we verify the rule. The agent cites the policy with a high Relevance Score of 92%, confirming the limit for Zylaria transfers is $5,000.",
    
    "07_Demo_AskAction": "Now, the real test. We ask: 'My client wants to send $4,000 to Zylaria. Is this allowed?' watch the sidebar.",
    
    "08_Demo_Result": "Boom. DENIED. The agent didn't just read the PDF. It checked the Live Ledger, found a prior $2,500 transfer, calculated the total exposure of $6,500, and blocked the transaction. This is Agentic Reasoning.",
    
    "09_Scenario2_Sanctions": "But it's not just about money. JurisLens creates a universal compliance layer. If I try to onboard a new client named Ivan Drago...",
    
    "10_Scenario2_Result": "It instantly switches tools, scans global sanctions lists, and flags him as a blocked entity. One agent, multiple defense lines.",
    
    "11_Closing": "Under the hood, we use Elasticsearch to scale to millions of documents with zero hallucination, and LangChain for orchestration.",
    
    "12_Adoption": "For Fintechs, adoption is seamless. Simply index your PDFs into Elastic Cloud, connect your ledger API to our Agent Tools, and you have an automated compliance officer running 24/7. Don't just chat with your data. Enforce it. This is JurisLens."
}

async def generate_audio():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print(f"[GENERATING] {len(SCRIPT)} audio files using {VOICE}...")
    
    for filename, text in SCRIPT.items():
        output_file = os.path.join(OUTPUT_DIR, f"{filename}.mp3")
        communicate = edge_tts.Communicate(text, VOICE)
        await communicate.save(output_file)
        print(f"[SAVED]: {output_file}")
        
    print("\n[DONE] All audio files generated in 'voiceovers/' folder!")

if __name__ == "__main__":
    asyncio.run(generate_audio())
