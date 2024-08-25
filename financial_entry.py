import logging

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []

    def add_salary(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        logging.info("Adding a new salary entry.")
        self.salary_entries.append({
            "gross_income": gross_income,
            "pension_contribution_percent": pension_contribution_percent,
            "company_match_percent": company_match_percent,
            "num_months": num_months
        })

    def add_expense(self, monthly_expense, num_months):
        logging.info("Adding a new expense entry.")
        self.expense_entries.append({
            "monthly_expense": monthly_expense,
            "num_months": num_months
        })

    def add_housing(self, house_name, house_value, deposit, mortgage_term, interest_rate, appreciation_rate, month_acquisition):
        logging.info("Adding a new housing entry.")
        self.housing_entries.append({
            "house_name": house_name,
            "house_value": house_value,
            "deposit": deposit,
            "mortgage_term": mortgage_term,
            "interest_rate": interest_rate,
            "appreciation_rate": appreciation_rate,
            "month_acquisition": month_acquisition
        })

    def calculate_tax(self, monthly_gross):
        # Placeholder implementation
        logging.info(f"Calculating tax for monthly gross income: {monthly_gross}")
        return monthly_gross * 0.2

    def calculate_ni(self, monthly_gross):
        # Placeholder implementation
        logging.info(f"Calculating National Insurance for monthly gross income: {monthly_gross}")
        return monthly_gross * 0.12
