import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


class UI:
    def __init__(self):
        pass

    def display(self):
        tab1, tab2, tab3, tab4 = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])
        with tab1:
            SalaryUI().display()
        with tab2:
            ExpensesUI().display()
        with tab3:
            HousingUI().display()
        with tab4:
            AnalysisUI().display()

class SalaryUI:
    def display(self, df_builder):
        st.header("Salary Input")
        with st.form(key="salary_form"):
            gross_income = st.number_input("Annual Gross Income", min_value=0.0, step=1000.0)
            pension_contribution_percent = st.number_input("Pension Contribution (%)", min_value=0.0, step=1.0)
            company_match_percent = st.number_input("Company Match (%)", min_value=0.0, step=1.0)
            num_months = st.number_input("Number of Months", min_value=1, step=1, key="salary_months")

            if st.form_submit_button("Add Salary"):
                st.session_state.financial_entry.add_salary_entry(gross_income, pension_contribution_percent,
                                                                  company_match_percent, num_months)

        combined_df = df_builder.rebuild_dataframe()
        st.dataframe(combined_df)
        st.line_chart(combined_df[["Salary", "Take Home Pay"]])


class ExpensesUI:
    def display(self, df_builder):
        st.header("Expenses Input")
        with st.form(key="expense_form"):
            monthly_expense = st.number_input("Monthly Expense", min_value=0.0, step=100.0)
            num_months = st.number_input("Number of Months", min_value=1, step=1, key="expense_months")

            if st.form_submit_button("Add Expense"):
                st.session_state.financial_entry.add_expense_entry(monthly_expense, num_months)

        combined_df = df_builder.rebuild_dataframe()
        st.dataframe(combined_df)
        st.line_chart(combined_df[["Expenses"]])


class HousingUI:
    def display(self, df_builder):
        st.header("Housing Input")
        st.write("Housing UI not yet implemented.")


class AnalysisUI:
    def display(self, df_builder):
        st.header("Analysis")

        data = {
            "x": list(range(1, 11)),
            "y1": list(range(1, 11)),
            "y2": [x ** 2 for x in range(1, 11)]
        }

        df = pd.DataFrame(data)
        st.dataframe(df)

        fig, ax = plt.subplots()
        ax.plot(df["x"], df["y1"], label="y1 = x")
        ax.plot(df["x"], df["y2"], label="y2 = x^2")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.legend()

        st.pyplot(fig)
