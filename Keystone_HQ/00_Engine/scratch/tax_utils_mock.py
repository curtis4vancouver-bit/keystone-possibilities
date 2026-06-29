def calculate_dividend_tax_benefit(salary: float, dividend: float) -> dict:
    """
    Calculates non-eligible dividend vs salary split tax benefits in British Columbia for 2026.
    A mock analytical tool to optimize the CCB (Canada Child Benefit) sweet spot.
    """
    if salary < 0 or dividend < 0:
        return {"error": "Income values must be non-negative"}
        
    total_income = salary + dividend
    # Non-eligible dividends receive a dividend tax credit but are grossed up
    gross_up_factor = 1.15
    taxable_dividend = dividend * gross_up_factor
    
    # Calculate simple federal/provincial brackets for 2026 (approximate simplified logic for testing)
    combined_taxable = salary + taxable_dividend
    
    # Simple bracket simulation
    if combined_taxable <= 45000:
        tax_rate = 0.20
    elif combined_taxable <= 90000:
        tax_rate = 0.282
    else:
        tax_rate = 0.38
        
    estimated_tax = (salary * tax_rate) + (taxable_dividend * (tax_rate - 0.05))
    after_tax_income = total_income - estimated_tax
    
    return {
        "total_income": total_income,
        "taxable_income": combined_taxable,
        "estimated_tax": float(round(estimated_tax, 2)),
        "after_tax_income": float(round(after_tax_income, 2)),
        "benefit_multiplier": 1.12 if combined_taxable < 60000 else 1.0
    }
