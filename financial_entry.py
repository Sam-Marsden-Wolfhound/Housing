import logging

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []

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

    def add_housing_entry(self, house_name, house_value, month_acquisition, appreciation_rate, sale, month_sale, mortgage, deposit, mortgage_term, standard_rate):
        entry = {
            "house_name": house_name,
            "house_value": house_value,
            "month_acquisition": month_acquisition,
            "appreciation_rate": appreciation_rate,
            "sale": sale,
            "month_sale": month_sale,
            "mortgage": mortgage,
            "deposit": deposit if mortgage else 0,
            "mortgage_term": mortgage_term if mortgage else 0,
            "standard_rate": standard_rate if mortgage else 0
        }
        self.housing_entries.append(entry)
        logging.info(f"Added housing entry: {entry}")

    def calculate_tax(self, gross_income):
        PERSONAL_ALLOWANCE = 12570
        BASIC_RATE_LIMIT = 50270
        HIGHER_RATE_LIMIT = 125140
        BASIC_RATE = 0.20
        HIGHER_RATE = 0.40
        ADDITIONAL_RATE = 0.45

        if gross_income <= PERSONAL_ALLOWANCE:
            return 0
        elif gross_income <= BASIC_RATE_LIMIT:
            return (gross_income - PERSONAL_ALLOWANCE) * BASIC_RATE
        elif gross_income <= HIGHER_RATE_LIMIT:
            return (BASIC_RATE_LIMIT - PERSONAL_ALLOWANCE) * BASIC_RATE + (gross_income - BASIC_RATE_LIMIT) * HIGHER_RATE
        else:
            return (BASIC_RATE_LIMIT - PERSONAL_ALLOWANCE) * BASIC_RATE + \
                (HIGHER_RATE_LIMIT - BASIC_RATE_LIMIT) * HIGHER_RATE + \
                (gross_income - HIGHER_RATE_LIMIT) * ADDITIONAL_RATE

    def calculate_ni(self, gross_income):
        NI_RATE = 0.12
        return gross_income * NI_RATE
