from langchain_core.tools import tool

@tool
def check_sanctions_tool(name: str) -> str:
    """
    Checks if a person or entity is on global sanctions lists (OFAC, UN, EU).
    Use this to validate new clients or counterparties during onboarding.
    
    Args:
        name: The name of the person or entity to check.
    """
    import time
    print(f"🕵️‍♀️ Scanning Global Sanctions Index for: '{name}'...")
    time.sleep(1.2) # Simulate search latency
    
    # Fake Database of Sanctioned Entities
    sanctioned_db = {
        "IVAN DRAGO": {"list": "OFAC SDN", "id": "RU-8821", "reason": "Connection to prohibited energy sector"},
        "VICTOR KRUM": {"list": "EU Watchlist", "id": "BG-9910", "reason": "High-risk politically exposed person"},
        "LE CHIFFRE": {"list": "Interpol Red", "id": "FR-007", "reason": "Terrorist financing"},
        "GOLIATH BANK": {"list": "Internal Blacklist", "id": "INT-001", "reason": "Conflict of interest"}
    }
    
    name_upper = name.upper().strip()
    
    if name_upper in sanctioned_db:
        record = sanctioned_db[name_upper]
        return (f"🚨 MATCH FOUND: '{name}' is a Sanctioned Entity.\n"
                f"Source: {record['list']}\n"
                f"ID: {record['id']}\n"
                f"Reason: {record['reason']}\n"
                f"Action: IMMEDIATE FREEZE required.")
    
    return f"✅ CLEAR. No matches found for '{name}' in global sanctions lists."
