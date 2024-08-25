import logging
import streamlit as st
from dataframe_builder import DataFrameBuilder

class SalaryUI:
    def display(self, df_builder):
        logging.info("Displaying Salary UI.")
        gross_income = st.number_input("Gross Income", min_value=0, step=100)
        pension_contribution = st.number_input("Pension Contribution (%)", min_value=0, max_value=100)
        company_match = st.number_input("Company Match (%)", min_value=0, max_value=100)
        num_months = st.number_input("Number of Months", min_value=1, step=1, key="salary_months")

        if st.button("Add Salary"):
            df_builder.add_salary_entry(gross_income, pension_contribution, company_match, num_months)
            st.session_state.df = df_builder.rebuild_dataframe()
            st.success("Salary entry added and DataFrame updated.")

class ExpensesUI:
    def display(self, df_builder):
        logging.info("Displaying Expenses UI.")
        monthly_expense = st.number_input("Monthly Expense", min_value=0, step=100)
        num_months = st.number_input("Number of Months", min_value=1, step=1, key="expense_months")

        if st.button("Add Expense"):
            df_builder.add_expense_entry(monthly_expense, num_months)
            st.session_state.df = df_builder.rebuild_dataframe()
            st.success("Expense entry added and DataFrame updated.")

class HousingUI:
    def display(self, df_builder):
        logging.info("Displaying Housing UI.")
        house_name = st.text_input("House Name")
        house_value = st.number_input("House Value", min_value=0, step=1000)
        deposit = st.number_input("Deposit", min_value=0, step=1000)
        mortgage_term = st.number_input("Mortgage Term (years)", min_value=0, step=1)
        standard_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.1)
        appreciation_rate = st.number_input("Appreciation Rate (%)", min_value=0.0, step=0.1)
        month_acquisition = st.number_input("Month of Acquisition", min_value=1, step=1)
        mortgage = st.checkbox("Include Mortgage")

        if st.button("Add House"):
            df_builder.add_housing_entry(house_name, house_value, deposit, mortgage_term, standard_rate,
                                         appreciation_rate, month_acquisition, mortgage)
            st.session_state.df = df_builder.rebuild_dataframe()
            st.success("House entry added and DataFrame updated.")

class AnalysisUI:
    def display(self, df_builder):
        logging.info("Displaying Analysis UI.")
        st.write("Analysis Tab - Placeholder for future enhancements.")

        # Placeholder DataFrame
        data = {
            "x": list(range(1, 11)),
            "y1": list(range(1, 11)),
            "y2": [x ** 2 for x in range(1, 11)]
        }
        df = pd.DataFrame(data)
        st.write(df)

        st.line_chart(df.set_index("x"))

        logging.info("Analysis UI displayed.")

