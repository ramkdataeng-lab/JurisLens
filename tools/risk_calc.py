from langchain_core.tools import tool

@tool
def calculate_risk_tool(amount: float, jurisdiction: str) -> str:
    """
    Checks the transaction against the Live Ledger and calculates compliance risk.
    Use this to validate if a specific transaction is safe given the client's history.
    
    Args:
        amount: The transaction amount.
        jurisdiction: The receiving country (e.g. "Zylaria").
    """
    import time
    
    # 1. Simulate API Latency
    print(f"🔌 Connecting to Core Banking Ledger... Looking up daily aggregates for {jurisdiction}...")
    time.sleep(1.0)
    
    # 2. Simulate "Live State" that Grok doesn't know
    # Pretend the client already sent money today
    prior_transfers = 0
    if "ZYLARIA" in jurisdiction.upper():
        prior_transfers = 2500.00
        print(f"⚠️ Found prior transaction today: ${prior_transfers:,.2f}")
    
    total_exposure = amount + prior_transfers
    
    # 3. Logic: Check Aggregate Limit ($5,000 usually)
    limit = 5000
    risk_level = "LOW"
    msg = ""
    
    if jurisdiction.upper() in ["NORTH KOREA", "IRAN", "SYRIA", "RUSSIA"]:
         return "Risk Level: CRITICAL. Sanctioned Jurisdiction. Blocked immediately."

    if total_exposure > limit:
        risk_level = "HIGH"
        msg = (f"TRANSGRESSION: Daily Aggregate Limit Exceeded.\n"
               f"Current Request: ${amount:,.2f}\n"
               f"Prior Today: ${prior_transfers:,.2f} (Found in Ledger)\n"
               f"Total exposure: ${total_exposure:,.2f} (Limit: ${limit:,.2f})")
    else:
        risk_level = "LOW"
        msg = (f"Safe. Total daily exposure ${total_exposure:,.2f} is within limit (${limit:,.2f}).\n"
               f"(Includes ${prior_transfers:,.2f} from prior transactions today).")

    return f"Risk Level: {risk_level}. {msg}"
