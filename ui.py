import streamlit as st
import pandas as pd
import logging

class SalaryUI:
    def display(self, df_builder):
        logging.info("Displaying Salary UI...")
        st.header("Salary Input")
        gross_income = st.number_input("Gross Annual Income", min_value=0, step=1000)
        pension_contribution_percent = st.number_input("Pension Contribution (%)", min_value=0.0, max_value=100.0, step=0.5)
        company_match_percent = st.number_input("Company Match (%)", min_value=0.0, max_value=100.0, step=0.5)
        num_months = st.number_input("Number of Months", min_value=1, step=1)

        if st.button("Add Salary"):
            df_builder.financial_entry.add_salary_entry(gross_income, pension_contribution_percent,
                                                        company_match_percent, num_months)
            st.session_state.df = df_builder.rebuild_dataframe()
            st.write(st.session_state.df)

class ExpensesUI:
    def display(self, df_builder):
        logging.info("Displaying Expenses UI...")
        st.header("Expenses Input")
        monthly_expense = st.number_input("Monthly Expense", min_value=0, step=100)
        start_month = st.number_input("Start Month", min_value=1, step=1)
        num_months = st.number_input("Number of Months", min_value=1, step=1)

        if st.button("Add Expense"):
            df_builder.financial_entry.add_expense_entry(monthly_expense, start_month, num_months)
            st.session_state.df = df_builder.rebuild_dataframe()
            st.write(st.session_state.df)

class HousingUI:
    def display(self, df_builder):
        logging.info("Displaying Housing UI...")
        st.header("Housing Input")

        if "house_counter" not in st.session_state:
            st.session_state.house_counter = 1

        new_house_name = st.sidebar.text_input("House Name", value=f"House {st.session_state.house_counter}")
        house_value = st.number_input("House Value", min_value=0, step=1000)
        deposit = st.number_input("Deposit", min_value=0, step=1000)
        mortgage_term = st.number_input("Mortgage Term (years)", min_value=1, step=1)
        standard_rate = st.number_input("Standard Rate (%)", min_value=0.0, max_value=100.0, step=0.5)
        appreciation_rate = st.number_input("Appreciation Rate (%)", min_value=0.0, max_value=100.0, step=0.5)
        month_acquisition = st.number_input("Month of Acquisition", min_value=1, step=1)
        mortgage = st.checkbox("Mortgage", value=True)

        if st.button("Add House"):
            df_builder.financial_entry.add_housing_entry(new_house_name, house_value, deposit, mortgage_term,
                                                         standard_rate, appreciation_rate, month_acquisition, mortgage)
            st.session_state.df = df_builder.rebuild_dataframe()
            st.write(st.session_state.df)
            st.session_state.house_counter += 1
