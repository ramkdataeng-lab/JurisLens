
from langchain_core.tools import Tool

def calculate_fine_risk(transaction_amount: float, jurisdiction: str) -> str:
    """
    Computes a risk score for a transaction.
    """
    risk_level = "LOW"
    fine_estimate = 0
    
    if jurisdiction.upper() in ["NORTH KOREA", "IRAN", "SYRIA"]:
        risk_level = "CRITICAL"
        fine_estimate = transaction_amount * 10
    elif transaction_amount > 10000:
        risk_level = "HIGH"
        fine_estimate = transaction_amount * 0.5
    elif transaction_amount > 2000:
        risk_level = "MEDIUM"
        fine_estimate = transaction_amount * 0.1
        
    return f"Risk Level: {risk_level}. Potential Fine: ${fine_estimate:,.2f} based on standard penalties."

def _risk_wrapper(input_str: str) -> str:
    """
    Wrapper for LLM tool usage. Input should be 'amount,jurisdiction' e.g. '5000,UK'
    """
    try:
        parts = input_str.split(",")
        amt = float(parts[0].strip())
        country = parts[1].strip()
        return calculate_fine_risk(amt, country)
    except:
        return "Error: Input format must be 'amount,country' (e.g. '5000,USA')"

calculate_risk_tool = Tool.from_function(
    func=_risk_wrapper,
    name="RiskCalculator",
    description="Calculates potential fines and risk levels. Input string format: 'amount,country' (e.g. '15000,Germany')."
)
