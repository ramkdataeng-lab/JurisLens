from fpdf import FPDF

def create_fake_pdf():
    pdf = FPDF()
    
    # Page 1
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "GOLIATH BANK - CONFIDENTIAL INTERNAL POLICY (2025)", ln=True, align='C')
    
    pdf.set_font("Arial", '', 12)
    pdf.ln(10) # Line break
    pdf.cell(0, 10, "This document contains sensitive internal procedures for AML compliance.", ln=True)
    pdf.cell(0, 10, "Unauthorized distribution is prohibited.", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Section 1: General Guidelines", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.multi_cell(0, 10, "All employees must report suspicious activity within 24 hours via Form X-99.")
    
    # Page 2
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Section 5: Project CHIMERA Protocol", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.ln(5)
    pdf.multi_cell(0, 10, "Due to recent geopolitical events, all transactions involving accounts originating from the unrecognized nation of 'Zylaria' are subject to Project CHIMERA scrutiny.")
    
    pdf.ln(5)
    pdf.multi_cell(0, 10, "Rule 5.1: Wire Transfer limits for Zylaria are capped at $5,000 USD.")
    pdf.multi_cell(0, 10, "Rule 5.2: Any transfer exceeding $5,000 requires written approval from the Regional Compliance Director (Level 4 Authorization).")
    pdf.multi_cell(0, 10, "Rule 5.3: The 'Blue Channel' reporting system must be used for these audits.")
    
    pdf.output("goliath_bank_internal_policy.pdf")
    print("PDF Generated: goliath_bank_internal_policy.pdf")

if __name__ == "__main__":
    create_fake_pdf()
