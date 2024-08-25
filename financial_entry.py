import logging

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []
        logging.info("FinancialEntry initialized.")

    def add_salary_entry(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        entry = {
            "gross_income": gross_income,
            "pension_contribution_percent": pension_contribution_percent,
            "company_match_percent": company_match_percent,
            "num_months": num_months
        }
        self.salary_entries.append(entry)
        logging.info(f"Added salary entry: {entry}")

    def add_expense_entry(self, monthly_expense, num_months):
        entry = {
            "monthly_expense": monthly_expense,
            "num_months": num_months
        }
        self.expense_entries.append(entry)
        logging.info(f"Added expense entry: {entry}")

    def add_housing_entry(self, house_name, house_value, deposit, mortgage_term, standard_rate, appreciation_rate, month_acquisition, mortgage):
        entry = {
            "house_name": house_name,
            "house_value": house_value,
            "deposit": deposit,
            "mortgage_term": mortgage_term,
            "standard_rate": standard_rate,
            "appreciation_rate": appreciation_rate,
            "month_acquisition": month_acquisition,
            "mortgage": mortgage
        }
        self.housing_entries.append(entry)
        logging.info(f"Added housing entry: {entry}")

    def calculate_tax(self, income):
        tax = income * 0.2
        logging.info(f"Calculated tax: {tax} for income: {income}")
        return tax

    def calculate_ni(self, income):
        ni = income * 0.12
        logging.info(f"Calculated NI: {ni} for income: {income}")
        return ni
