
import asyncio
import edge_tts
import os

# Select Voice: 
# "en-US-ChristopherNeural" (Male, Professional)
# "en-US-JennyNeural" (Female, Clear)
VOICE = "en-US-ChristopherNeural"
OUTPUT_DIR = "voiceovers"

SCRIPT = {
    "01_Intro": "Web search engines are great at reading, but terrible at enforcing. Meet JurisLens: The first Autonomous Compliance Agent powered by the Elastic Agent Builder.",
    
    "02_TheProblem": "We all know LLMs can read. I can feed a 50-page banking regulation PDF into a standard chatbot and ask if a $4,000 transfer is allowed. It will read the rule limit of $5,000 and say YES. But in the real world, compliance isn't just about reading rules. It's about knowing the state of the enterprise.",
    
    "03_TheBlindSpot": "The chatbot is state-blind. It doesn't know that this specific client already transferred $2,500 this morning. It inadvertently approves a transaction that actually violates the enterprise limit.",
    
    "04_Solution": "Enter JurisLens Pro. Built on Elastic Agent Builder, it uses ELSER v2—Elastic's latest semantic model—to understand the intent behind complex statutes. It doesn't just match keywords; it understands the law.",
    
    "05_Demo_Ingest": "Watch this. We ingest a confidential bank policy PDF. JurisLens indexes it instantly into Elasticsearch, optimized for high-precision semantic retrieval.",
    
    "06_Demo_AskRule": "First, we verify the rule. The agent identifies the regulation with a semantic relevance score of 98%, confirming the $5,000 limit for Zylaria transfers.",
    
    "07_Demo_AskAction": "Now, the real test. We ask: 'My client wants to send $4,000 to Zylaria. Is this allowed?' Check the terminal.",
    
    "08_Demo_Result": "Boom. DENIED. JurisLens executed a live ES|QL query against our transaction logs. It found a prior $2,500 transfer, calculated the total exposure of $6,500, and blocked the transaction. This is true Agentic Reasoning.",
    
    "09_Scenario2_Sanctions": "But it's not just about money. JurisLens acts as a universal orchestrator. If I try to onboard a new client named Ivan Drago...",
    
    "10_Scenario2_Result": "It instantly switches tools, scans global sanctions lists, and flags him as a high-risk entity. One unified agent, multiple lines of defense.",
    
    "11_Closing": "By leveraging Elasticsearch as our backbone, we ensure zero hallucination and provide perfect audit trails with page-level citations.",
    
    "12_Adoption": "For Fintechs, adoption is seamless. Simply index your policies into Elastic Cloud, connect your ledger to our ES|QL Agent Tools, and you have an automated compliance officer running 24/7. Visit jurislens dot vercel dot app to see it in action. Don't just chat with your data. Enforce it. This is JurisLens."
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
