import streamlit as st
from dataframe_builder import DataFrameBuilder
import logging

class SalaryUI:
    def display(self, df_builder: DataFrameBuilder):
        st.title("Salary Management")

        gross_income = st.number_input("Gross Income", min_value=0)
        pension_contribution_percent = st.number_input("Pension Contribution (%)", min_value=0, max_value=100)
        company_match_percent = st.number_input("Company Match (%)", min_value=0, max_value=100)
        num_months = st.number_input("Number of Months", min_value=1, step=1)

        if st.button("Add Salary"):
            st.session_state.df_salary = df_builder.add_salary_entry(
                gross_income, pension_contribution_percent, company_match_percent, num_months
            )
            logging.info("Added salary entry")

        st.dataframe(st.session_state.df_salary)

        # Graph Placeholder
        st.line_chart(st.session_state.df_salary)

class ExpensesUI:
    def display(self, df_builder: DataFrameBuilder):
        st.title("Expenses Management")

        monthly_expense = st.number_input("Monthly Expense", min_value=0)
        num_months = st.number_input("Number of Months", min_value=1, step=1)

        if st.button("Add Expense"):
            st.session_state.df_expenses = df_builder.add_expense_entry(monthly_expense, num_months)
            logging.info("Added expense entry")

        st.dataframe(st.session_state.df_expenses)

        # Graph Placeholder
        st.line_chart(st.session_state.df_expenses)

class HousingUI:
    def display(self, df_builder: DataFrameBuilder):
        st.title("Housing Management")

        house_name = st.text_input("House Name")
        house_value = st.number_input("House Value", min_value=0)
        deposit = st.number_input("Deposit", min_value=0)
        mortgage_term = st.number_input("Mortgage Term (years)", min_value=0)
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, max_value=100.0)
        appreciation_rate = st.number_input("Appreciation Rate (%)", min_value=0.0, max_value=100.0)
        month_acquisition = st.number_input("Month of Acquisition", min_value=1)

        if st.button("Add House"):
            st.session_state.df_housing = df_builder.add_housing_entry(
                house_name, house_value, deposit, mortgage_term, interest_rate, appreciation_rate, month_acquisition
            )
            logging.info("Added housing entry")

        st.dataframe(st.session_state.df_housing)

        # Graph Placeholder
        st.line_chart(st.session_state.df_housing)

class AnalysisUI:
    def display(self):
        st.title("Analysis")

        # Placeholder DataFrame and Graph
        import pandas as pd

        data = {
            "x": range(1, 11),
            "y1": range(1, 11),
            "y2": [i ** 2 for i in range(1, 11)],
        }
        df = pd.DataFrame(data)
        st.dataframe(df)

        st.line_chart(df)
