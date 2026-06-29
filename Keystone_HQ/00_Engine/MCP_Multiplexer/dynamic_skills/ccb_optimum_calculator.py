"""
Evolved Dynamic Skill: ccb_optimum_calculator
Description: CCB & Tax Optimization sweet spot calculator
"""

#!/usr/bin/env python3
"""
CCB and Tax Optimum Calculator (British Columbia - 2025/2026 Rates)
Specifically designed for Wayne to evaluate the mathematical sweet spot 
between T4 Salary and T5 Non-Eligible Dividends from a CCPC in BC.
"""

import sys

# 2025/2026 BC and Federal Tax Brackets & Rates
FED_BASIC_PERSONAL_AMOUNT = 15705.0
BC_BASIC_PERSONAL_AMOUNT = 12906.0

# CPP Rates (2026)
CPP_EXEMPTION = 3500.0
CPP_EMPLOYEE_RATE = 0.0595  # 5.95%
CPP_EMPLOYER_RATE = 0.0595  # 5.95%
CPP_MAX_SALARY_BASE = 71300.0  # Approx YMPE for 2026

# Non-Eligible Dividend Parameters
DIV_GROSS_UP_RATE = 1.15  # 15% Gross-Up
FED_DIV_TAX_CREDIT_RATE = 0.090301  # 9.0301% of grossed-up dividend
BC_DIV_TAX_CREDIT_RATE = 0.0196  # 1.96% of grossed-up dividend

# Corporate Small Business Tax Rate (BC)
CORP_TAX_RATE_BC = 0.11  # 11% combined federal/provincial SBD rate

def model_scenario(desired_personal_cash, compensation_type, num_children=2, children_under_6=1):
    """
    Models the complete tax and benefit ecosystem for a specific net cash transfer.
    """
    if compensation_type == "salary":
        # Salary (T4): Cash personal = Salary - Personal Tax - Employee CPP
        # Note: Salary is a deductible business expense, saving corporate tax at 11%.
        # To find the gross salary required to yield 'desired_personal_cash', we iterate.
        gross_salary = desired_personal_cash
        step = 100.0
        for _ in range(1000):
            # Calculate CPP on gross
            pensionable = min(gross_salary, CPP_MAX_SALARY_BASE)
            cpp_employee = max(0.0, (pensionable - CPP_EXEMPTION) * CPP_EMPLOYEE_RATE)
            cpp_employer = cpp_employee # Employer matches CPP
            
            tax = calculate_personal_tax_bc(gross_salary, dividend_cash=0.0)
            net_personal = gross_salary - tax - cpp_employee
            
            if abs(net_personal - desired_personal_cash) < 10.0:
                break
            elif net_personal < desired_personal_cash:
                gross_salary += step
            else:
                gross_salary -= step
                step /= 2.0
                
        # Total cost to corporation for salary
        corp_cost = gross_salary + cpp_employer
        # Corporate tax saving (salary + employer CPP are corporate expenses)
        corp_tax_saving = corp_cost * CORP_TAX_RATE_BC
        net_corp_drain = corp_cost - corp_tax_saving
        
        # AFNI for CCB is net personal income (Line 23600), which is roughly equal to gross salary
        afni = gross_salary
        personal_tax = tax
        cpp_total = cpp_employee + cpp_employer
        dividend_grossup_drag = 0.0
        
    else:  # "dividend" (T5)
        # Dividends are paid from post-tax corporate income. No CPP is paid.
        # To yield 'desired_personal_cash', personal tax is paid on the grossed-up dividend.
        dividend_cash = desired_personal_cash
        step = 100.0
        for _ in range(1000):
            tax = calculate_personal_tax_bc(0.0, dividend_cash=dividend_cash)
            net_personal = dividend_cash - tax
            
            if abs(net_personal - desired_personal_cash) < 10.0:
                break
            elif net_personal < desired_personal_cash:
                dividend_cash += step
            else:
                dividend_cash -= step
                step /= 2.0
                
        # To distribute this dividend, the corp must have earned it pre-tax.
        # Pre-tax corporate earnings required = dividend_cash / (1 - CORP_TAX_RATE_BC)
        corp_pretax_required = dividend_cash / (1.0 - CORP_TAX_RATE_BC)
        corp_tax_paid = corp_pretax_required * CORP_TAX_RATE_BC
        net_corp_drain = corp_pretax_required
        
        # AFNI for CCB is grossed-up dividend
        afni = dividend_cash * DIV_GROSS_UP_RATE
        personal_tax = tax
        cpp_total = 0.0
        dividend_grossup_drag = afni - dividend_cash
        
    # Calculate child benefits based on AFNI
    ccb_amount = calculate_ccb(afni, num_children, children_under_6)
    bcfb_amount = calculate_bc_family_benefit(afni, num_children)
    total_benefits = ccb_amount + bcfb_amount
    
    # Net Family Wealth Position
    # (Net personal cash + family benefits) - Net corporate pre-tax drain
    net_family_wealth = desired_personal_cash + total_benefits - net_corp_drain
    
    return {
        "gross_equivalent": gross_salary if compensation_type == "salary" else dividend_cash,
        "afni": afni,
        "personal_tax": personal_tax,
        "cpp_total": cpp_total,
        "dividend_grossup_drag": dividend_grossup_drag,
        "ccb": ccb_amount,
        "bcfb": bcfb_amount,
        "total_benefits": total_benefits,
        "net_corp_drain": net_corp_drain,
        "net_family_wealth": net_family_wealth,
        "net_pocket_cash": desired_personal_cash + total_benefits
    }

def calculate_personal_tax_bc(taxable_income, dividend_cash=0.0):
    """
    Calculates BC and Federal Personal Income Tax, taking into account
    Basic Personal Amounts and Dividend Tax Credits for non-eligible dividends.
    """
    # Gross up dividends if any
    grossed_up_div = dividend_cash * DIV_GROSS_UP_RATE
    total_taxable_income = taxable_income + grossed_up_div
    
    # 1. Federal Income Tax (2025/2026 brackets)
    # Brackets: 15% up to $55,867
    fed_tax = 0.0
    if total_taxable_income <= 55867.0:
        fed_tax = total_taxable_income * 0.15
    else:
        fed_tax = 55867.0 * 0.15 + (total_taxable_income - 55867.0) * 0.205
        
    # Federal basic personal credit
    fed_credit = min(total_taxable_income, FED_BASIC_PERSONAL_AMOUNT) * 0.15
    fed_tax = max(0.0, fed_tax - fed_credit)
    
    # 2. BC Provincial Income Tax (2025/2026 brackets)
    # Brackets: 5.06% up to $47,579
    bc_tax = 0.0
    if total_taxable_income <= 47579.0:
        bc_tax = total_taxable_income * 0.0506
    else:
        bc_tax = 47579.0 * 0.0506 + (total_taxable_income - 47579.0) * 0.077
        
    # BC basic personal credit
    bc_credit = min(total_taxable_income, BC_BASIC_PERSONAL_AMOUNT) * 0.0506
    bc_tax = max(0.0, bc_tax - bc_credit)
    
    # 3. Apply Dividend Tax Credits
    if dividend_cash > 0.0:
        fed_dtc = grossed_up_div * FED_DIV_TAX_CREDIT_RATE
        bc_dtc = grossed_up_div * BC_DIV_TAX_CREDIT_RATE
        
        fed_tax = max(0.0, fed_tax - fed_dtc)
        bc_tax = max(0.0, bc_tax - bc_dtc)
        
    total_tax = fed_tax + bc_tax
    return total_tax

def calculate_ccb(afni, num_children=2, children_under_6=1):
    """
    Calculates Canada Child Benefit (CCB) based on Adjusted Family Net Income (AFNI).
    Rates reflect the 2025/2026 benefit year.
    """
    # Max benefits per child
    max_under_6 = 7782.0
    max_over_6 = 6570.0
    
    under_6 = children_under_6
    over_6 = max(0, num_children - under_6)
    
    max_ccb = (under_6 * max_under_6) + (over_6 * max_over_6)
    
    # Reduction formulas based on number of kids
    reduction = 0.0
    if afni <= 36502.0:
        reduction = 0.0
    elif afni <= 75537.0:
        excess = afni - 36502.0
        if num_children == 1:
            reduction = excess * 0.07
        elif num_children == 2:
            reduction = excess * 0.135
        elif num_children == 3:
            reduction = excess * 0.19
        else:
            reduction = excess * 0.23
    else:
        # Excess above Threshold 2
        excess_t2 = afni - 75537.0
        if num_children == 1:
            reduction = (75537.0 - 36502.0) * 0.07 + excess_t2 * 0.032
        elif num_children == 2:
            reduction = (75537.0 - 36502.0) * 0.135 + excess_t2 * 0.057
        elif num_children == 3:
            reduction = (75537.0 - 36502.0) * 0.19 + excess_t2 * 0.08
        else:
            reduction = (75537.0 - 36502.0) * 0.23 + excess_t2 * 0.095
            
    final_ccb = max(0.0, max_ccb - reduction)
    return final_ccb

def calculate_bc_family_benefit(afni, num_children=2):
    """
    Calculates BC Family Benefit (BCFB) based on AFNI.
    """
    # Max benefits (2025/2026 approximate baseline)
    if num_children == 1:
        max_bcfb = 1850.0
    elif num_children == 2:
        max_bcfb = 3250.0
    elif num_children >= 3:
        max_bcfb = 3250.0 + (num_children - 2) * 1200.0
    else:
        return 0.0
        
    # Clawback starts at $29,662
    reduction = 0.0
    if afni > 29662.0:
        excess = afni - 29662.0
        # Clawback rate is roughly 4% per child up to max amount
        reduction_rate = 0.04 * num_children
        reduction = excess * reduction_rate
        
    final_bcfb = max(0.0, max_bcfb - reduction)
    return final_bcfb

def print_dashboard(target_cash, num_kids=2, kids_under_6=1):
    print("=" * 80)
    print(f" COMPENSATION ARCHITECTURE DASHBOARD: TARGETING ${target_cash:,.2f} NET PERSONAL CASH")
    print(f" Setup: {num_kids} Children ({kids_under_6} Under 6 Years Old) in British Columbia")
    print("=" * 80)
    
    sal = model_scenario(target_cash, "salary", num_kids, kids_under_6)
    div = model_scenario(target_cash, "dividend", num_kids, kids_under_6)
    
    print(f"{'Metric':<35} | {'T4 Salary Route':<20} | {'T5 Dividend Route':<20}")
    print("-" * 80)
    print(f"{'Gross Declared Compensation':<35} | ${sal['gross_equivalent']:<19,.2f} | ${div['gross_equivalent']:<19,.2f}")
    print(f"{'Adjusted Family Net Income (AFNI)':<35} | ${sal['afni']:<19,.2f} | ${div['afni']:<19,.2f}")
    print(f"{'Dividend Gross-Up Penalty Drag':<35} | ${sal['dividend_grossup_drag']:<19,.2f} | ${div['dividend_grossup_drag']:<19,.2f}")
    print("-" * 80)
    print(f"{'Personal Income Tax (Federal + BC)':<35} | ${sal['personal_tax']:<19,.2f} | ${div['personal_tax']:<19,.2f}")
    print(f"{'Canada Pension Plan (CPP) Paid':<35} | ${sal['cpp_total']:<19,.2f} | ${div['cpp_total']:<19,.2f}")
    print("-" * 80)
    print(f"{'Canada Child Benefit (CCB) Yield':<35} | ${sal['ccb']:<19,.2f} | ${div['ccb']:<19,.2f}")
    print(f"{'BC Family Benefit Yield':<35} | ${sal['bcfb']:<19,.2f} | ${div['bcfb']:<19,.2f}")
    print(f"{'Total Government Benefits Cash':<35} | ${sal['total_benefits']:<19,.2f} | ${div['total_benefits']:<19,.2f}")
    print("-" * 80)
    print(f"{'Net Corporate Pre-Tax Cash Drain':<35} | ${sal['net_corp_drain']:<19,.2f} | ${div['net_corp_drain']:<19,.2f}")
    print(f"{'TOTAL NET CASH IN POCKET':<35} | ${sal['net_pocket_cash']:<19,.2f} | ${div['net_pocket_cash']:<19,.2f}")
    print(f"{'Net Family Wealth Efficiency':<35} | ${sal['net_family_wealth']:<19,.2f} | ${div['net_family_wealth']:<19,.2f}")
    print("=" * 80)
    
    # Structural Analysis Commentary
    print("\nPRO CA-LEVEL STRATEGY ANALYSIS:")
    
    # 1. The Low Income Sweet Spot ($22,000 baseline)
    if target_cash <= 25000:
        print(f"--> [SWEET SPOT DETECTED] At ${target_cash:,.0f} net, personal tax is $0 for both routes because of the Basic Personal Amount.")
        print(f"--> [CPP SAVINGS WINS] Dividend route completely bypasses CPP, saving ${sal['cpp_total']:,.2f} in combined payroll taxes.")
        print(f"--> [CCB GROSS-UP IMPACT] However, the dividend route gross-up increases AFNI from ${sal['gross_equivalent']:,.0f} to ${div['afni']:,.0f}.")
        benefit_diff = sal['total_benefits'] - div['total_benefits']
        if benefit_diff > 0:
            print(f"    This gross-up reduces your child benefits by ${benefit_diff:,.2f} compared to the salary route.")
        else:
            print("    Your income is low enough that BOTH routes remain under the $29,662/yr threshold for 100% maximum benefits!")
            
        net_efficiency = div['net_family_wealth'] - sal['net_family_wealth']
        if net_efficiency > 0:
            print(f"--> [RECOMMENDATION: DIVIDENDS] Overall, the dividend route is ${net_efficiency:,.2f} more efficient for the family because CPP savings drastically outweigh the CCB impact.")
        else:
            print(f"--> [RECOMMENDATION: SALARY] Overall, the salary route is ${abs(net_efficiency):,.2f} more efficient due to maximizing child benefits.")
    else:
        print("--> For higher cash ranges, the clawback of CCB and the introduction of personal income tax makes salary increasingly viable as a direct corporate expense deduction, but dividends remain a strong way to skip the mandatory employee/employer CPP premium.")
        
    print("=" * 80)

if __name__ == "__main__":
    target = 22000.0
    if len(sys.argv) > 1:
        try:
            target = float(sys.argv[1])
        except ValueError:
            pass
            
    print_dashboard(target, num_kids=2, kids_under_6=1)
