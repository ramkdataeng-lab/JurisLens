from langchain_core.tools import tool

@tool
def calculate_risk_tool(amount: float, jurisdiction: str) -> str:
    """
    Calculates the financial compliance risk and potential fine based on transaction amount and jurisdiction.
    Use this tool when the user asks about risk levels or fines for a specific transfer.
    
    Args:
        amount: The transaction amount as a number (e.g. 50000).
        jurisdiction: The receiving country or region (e.g. "France").
    """
    risk_level = "LOW"
    fine_estimate = 0
    
    # Simple logic for demo purposes
    if jurisdiction.upper() in ["NORTH KOREA", "IRAN", "SYRIA", "RUSSIA"]:
        risk_level = "CRITICAL"
        fine_estimate = amount * 10
    elif amount > 10000:
        risk_level = "HIGH"
        fine_estimate = amount * 0.5
    elif amount > 2000:
        risk_level = "MEDIUM"
        fine_estimate = amount * 0.1
        
    return f"Risk Level: {risk_level}. Potential Fine: ${fine_estimate:,.2f} based on standard penalties."
