from tax_calculator import TaxCalculator

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []

    def add_salary(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        self.salary_entries.append({
            "gross_income": gross_income,
            "pension_contribution_percent": pension_contribution_percent,
            "company_match_percent": company_match_percent,
            "num_months": num_months
        })

    def add_expense(self, monthly_expense, num_months):
        self.expense_entries.append({
            "monthly_expense": monthly_expense,
            "num_months": num_months
        })

    def add_house(self, house_name, house_value, month_acquisition, appreciation_rate,
                  sale, month_sale, mortgage, deposit, mortgage_term, standard_rate):
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
