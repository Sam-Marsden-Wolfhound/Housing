import logging

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []

    def add_salary_entry(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        logging.info(f"Adding salary entry: gross_income={gross_income}, pension_contribution_percent={pension_contribution_percent}, company_match_percent={company_match_percent}, num_months={num_months}")
        self.salary_entries.append({
            "gross_income": gross_income,
            "pension_contribution_percent": pension_contribution_percent,
            "company_match_percent": company_match_percent,
            "num_months": num_months
        })

    def add_expense_entry(self, monthly_expense, num_months):
        logging.info(f"Adding expense entry: monthly_expense={monthly_expense}, num_months={num_months}")
        self.expense_entries.append({
            "monthly_expense": monthly_expense,
            "num_months": num_months
        })

    def calculate_tax(self, monthly_gross):
        logging.info(f"Calculating tax for monthly_gross={monthly_gross}")
        # Simplified tax calculation
        return monthly_gross * 0.2

    def calculate_ni(self, monthly_gross):
        logging.info(f"Calculating National Insurance for monthly_gross={monthly_gross}")
        # Simplified NI calculation
        return monthly_gross * 0.12
