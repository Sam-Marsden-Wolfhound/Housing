import streamlit as st
from dataframe_builder import DataFrameBuilder


class SalaryUI:
    def display(self, df_builder):
        st.header("Salary Inputs")
        gross_income = st.number_input("Gross Income", min_value=0, step=1000, key="salary_gross_income")
        pension_contribution_percent = st.number_input("Pension Contribution (%)", min_value=0, max_value=100, step=1,
                                                       key="pension_contribution_percent")
        company_match_percent = st.number_input("Company Match (%)", min_value=0, max_value=100, step=1,
                                                key="company_match_percent")
        num_months = st.number_input("Number of Months", min_value=1, step=1, key="salary_num_months")

        if st.button("Add Salary", key="add_salary"):
            st.session_state.df = df_builder.add_salary_entry(
                gross_income,
                pension_contribution_percent,
                company_match_percent,
                num_months
            )
            st.success("Salary added successfully")


class ExpensesUI:
    def display(self, df_builder):
        st.header("Expenses Inputs")
        monthly_expense = st.number_input("Monthly Expense", min_value=0, step=100, key="monthly_expense")
        num_months = st.number_input("Number of Months", min_value=1, step=1, key="expenses_num_months")

        if st.button("Add Expense", key="add_expense"):
            st.session_state.df = df_builder.add_expense_entry(monthly_expense, num_months)
            st.success("Expense added successfully")


class HousingUI:
    def display(self, df_builder):
        st.header("Housing Inputs")

        if 'house_counter' not in st.session_state:
            st.session_state.house_counter = 1

        new_house_name = st.sidebar.text_input("House Name", value=f"House {st.session_state.house_counter}")
        house_value = st.number_input("House Value", min_value=0, step=1000,
                                      key=f"house_value_{st.session_state.house_counter}")
        deposit = st.number_input("Deposit", min_value=0, step=1000, key=f"deposit_{st.session_state.house_counter}")
        mortgage_term = st.number_input("Mortgage Term (years)", min_value=0, step=1,
                                        key=f"mortgage_term_{st.session_state.house_counter}")
        interest_rate = st.number_input("Interest Rate (%)", min_value=0.0, step=0.1,
                                        key=f"interest_rate_{st.session_state.house_counter}")
        appreciation_rate = st.number_input("Appreciation Rate (%)", min_value=0.0, step=0.1,
                                            key=f"appreciation_rate_{st.session_state.house_counter}")
        month_acquisition = st.number_input("Month of Acquisition", min_value=0, step=1,
                                            key=f"month_acquisition_{st.session_state.house_counter}")
        mortgage = st.checkbox("Mortgage", key=f"mortgage_{st.session_state.house_counter}")

        if st.button("Add House", key=f"add_house_{st.session_state.house_counter}"):
            st.session_state.df = df_builder.add_house_entry(
                new_house_name,
                house_value,
                deposit,
                mortgage_term,
                interest_rate,
                appreciation_rate,
                month_acquisition,
                mortgage
            )
            st.session_state.house_counter += 1
            st.success("House added successfully")

