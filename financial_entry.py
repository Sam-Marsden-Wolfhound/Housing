import logging
import streamlit as st
from tax_calculator import TaxCalculator

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FinancialEntry:
    def __init__(self):
        self.salary_entries = []
        self.expense_entries = []
        self.housing_entries = []

        # Initialize session state for salary, expenses, and housing
        if "salary_entries" not in st.session_state:
            st.session_state.salary_entries = []
        if "expense_entries" not in st.session_state:
            st.session_state.expense_entries = []
        if "housing_entries" not in st.session_state:
            st.session_state.housing_entries = []
        if "house_counter" not in st.session_state:
            st.session_state.house_counter = 1

    def add_salary_entry(self, gross_income, pension_contribution_percent, company_match_percent, num_months):
        logging.info(f"Adding salary entry: gross_income={gross_income}, "
                     f"pension_contribution_percent={pension_contribution_percent}, "
                     f"company_match_percent={company_match_percent}, num_months={num_months}")

        salary_entry = {
            "gross_income": gross_income,
            "pension_contribution_percent": pension_contribution_percent,
            "company_match_percent": company_match_percent,
            "num_months": num_months
        }

        self.salary_entries.append(salary_entry)
        st.session_state.salary_entries.append(salary_entry)

    def add_expense_entry(self, monthly_expense, num_months):
        logging.info(f"Adding expense entry: monthly_expense={monthly_expense}, num_months={num_months}")

        expense_entry = {
            "monthly_expense": monthly_expense,
            "num_months": num_months
        }

        self.expense_entries.append(expense_entry)
        st.session_state.expense_entries.append(expense_entry)

    def add_housing_entry(self, house_name, house_value, month_acquisition, appreciation_rate,
                          sale, month_sale, mortgage, deposit, mortgage_term, standard_rate):
        logging.info(f"Adding housing entry: house_name={house_name}, house_value={house_value}, "
                     f"month_acquisition={month_acquisition}, appreciation_rate={appreciation_rate}, "
                     f"sale={sale}, month_sale={month_sale}, mortgage={mortgage}, deposit={deposit}, "
                     f"mortgage_term={mortgage_term}, standard_rate={standard_rate}")

        housing_entry = {
            "house_name": house_name,
            "house_value": house_value,
            "month_acquisition": month_acquisition,
            "appreciation_rate": appreciation_rate,
            "sale": sale,
            "month_sale": month_sale,
            "mortgage": mortgage,
            "deposit": deposit,
            "mortgage_term": mortgage_term,
            "standard_rate": standard_rate
        }

        self.housing_entries.append(housing_entry)
        st.session_state.housing_entries.append(housing_entry)

    def calculate_tax(self, gross_income):
        return TaxCalculator.calculate_tax(gross_income)

    def calculate_ni(self, gross_income):
        return TaxCalculator.calculate_ni(gross_income)
