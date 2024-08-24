import logging
from tax_calculator import TaxCalculator

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []

    def add_salary_entry(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        logging.info(f"Adding salary entry: gross_income={gross_income}, pension_contribution_percent={pension_contribution_percent}, "
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
        logging.info(f"Adding housing entry: house_name={house_name}, house_value={house_value}, month_acquisition={month_acquisition}, "
                     f"appreciation_rate={appreciation_rate}, sale={sale}, month_sale={month_sale}, mortgage={mortgage}, "
                     f"deposit={deposit}, mortgage_term={mortgage_term}, standard_rate={standard_rate}")
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

    def calculate_tax(self, gross_income):
        tax = TaxCalculator.calculate_tax(gross_income)
        logging.info(f"Calculated tax for gross_income={gross_income}: {tax}")
        return tax

    def calculate_ni(self, gross_income):
        ni = TaxCalculator.calculate_ni(gross_income)
        logging.info(f"Calculated NI for gross_income={gross_income}: {ni}")
        return ni
