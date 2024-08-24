import logging

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []

    def add_salary_entry(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        logging.info(f"Adding salary entry: gross_income={gross_income}, "
                     f"pension_contribution_percent={pension_contribution_percent}, "
                     f"company_match_percent={company_match_percent}, num_months={num_months}")
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

    def add_housing_entry(self, house_name, house_value, month_acquisition, appreciation_rate, sale, month_sale, mortgage, deposit, mortgage_term, standard_rate):
        logging.info(f"Adding housing entry: house_name={house_name}, house_value={house_value}, "
                     f"month_acquisition={month_acquisition}, appreciation_rate={appreciation_rate}, sale={sale}, "
                     f"month_sale={month_sale}, mortgage={mortgage}, deposit={deposit}, mortgage_term={mortgage_term}, "
                     f"standard_rate={standard_rate}")
        self.housing_entries.append({
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
        })

    # Tax and NI calculations as per the UK 2024 tax and NI rates
    @staticmethod
    def calculate_tax(gross_income):
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

    @staticmethod
    def calculate_ni(gross_income):
        NI_RATE = 0.12
        return gross_income * NI_RATE
