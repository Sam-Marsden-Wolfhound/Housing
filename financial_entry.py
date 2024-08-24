import logging

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []

    def add_salary_entry(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        logging.info(f"Adding salary entry: gross_income={gross_income}, "
                     f"pension_contribution_percent={pension_contribution_percent}, "
                     f"company_match_percent={company_match_percent}, num_months={num_months}")
        entry = {
            "gross_income": gross_income,
            "pension_contribution_percent": pension_contribution_percent,
            "company_match_percent": company_match_percent,
            "num_months": num_months
        }
        self.salary_entries.append(entry)

    def add_expense_entry(self, monthly_expense, num_months):
        logging.info(f"Adding expense entry: monthly_expense={monthly_expense}, num_months={num_months}")
        entry = {
            "monthly_expense": monthly_expense,
            "num_months": num_months
        }
        self.expense_entries.append(entry)

    def add_housing_entry(self, house_name, house_value, appreciation_rate, month_acquisition, mortgage=False,
                          deposit=0, mortgage_term=0, standard_rate=0):
        logging.info(f"Adding housing entry: house_name={house_name}, house_value={house_value}, "
                     f"appreciation_rate={appreciation_rate}, month_acquisition={month_acquisition}, "
                     f"mortgage={mortgage}, deposit={deposit}, mortgage_term={mortgage_term}, "
                     f"standard_rate={standard_rate}")
        entry = {
            "house_name": house_name,
            "house_value": house_value,
            "appreciation_rate": appreciation_rate,
            "month_acquisition": month_acquisition,
            "mortgage": mortgage,
            "deposit": deposit,
            "mortgage_term": mortgage_term,
            "standard_rate": standard_rate
        }
        self.housing_entries.append(entry)

    def calculate_tax(self, monthly_gross):
        # A placeholder tax calculation formula
        tax = monthly_gross * 0.2
        logging.info(f"Calculating tax for monthly_gross={monthly_gross}: {tax}")
        return tax

    def calculate_ni(self, monthly_gross):
        # A placeholder national insurance calculation formula
        ni = monthly_gross * 0.12
        logging.info(f"Calculating national insurance for monthly_gross={monthly_gross}: {ni}")
        return ni
