from fpdf import FPDF

def create_global_standard_pdf():
    pdf = FPDF()
    pdf.add_page()
    
    # Title
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "GLOBAL FINANCIAL CRIME STANDARDS (2025 Edition)", ln=True, align='C')
    pdf.ln(10)
    
    # Body
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, "This document outlines the mandatory minimum standards for all financial institutions operating within the G20 nations.")
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Section 19: High-Risk Jurisdictions", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, "Financial institutions must apply enhanced due diligence to business relationships and transactions with natural and legal persons from countries for which this is called for by the FATF.")
    
    pdf.ln(5)
    pdf.multi_cell(0, 10, "Standard 19.3: Unrecognized Territories (e.g., Zylaria, Atlantis)")
    pdf.multi_cell(0, 10, "Transactions involving unrecognized territories pose significant money laundering risks. To mitigate this:")
    pdf.multi_cell(0, 10, "1. Wire transfers must not exceed $10,000 USD per day without Enhanced Due Diligence (EDD).")
    pdf.multi_cell(0, 10, "2. Any transfer above this threshold requires filing a Suspicious Activity Report (SAR).")
    
    pdf.output("global_regulation_standard.pdf")
    print("PDF Generated: global_regulation_standard.pdf")

if __name__ == "__main__":
    create_global_standard_pdf()
