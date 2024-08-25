import streamlit as st
from ui import SalaryUI, ExpensesUI, HousingUI, AnalysisUI
from dataframe_builder import DataFrameBuilder
from financial_entry import FinancialEntry

def main():
    st.set_page_config(layout="wide")
    df_builder = DataFrameBuilder(FinancialEntry())

    st.session_state.df_salary = df_builder.build_empty_dataframe()
    st.session_state.df_expenses = df_builder.build_empty_dataframe()
    st.session_state.df_housing = df_builder.build_empty_dataframe()

    tabs = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])

    with tabs[0]:
        SalaryUI().display(df_builder)

    with tabs[1]:
        ExpensesUI().display(df_builder)

    with tabs[2]:
        HousingUI().display(df_builder)

    with tabs[3]:
        AnalysisUI().display()

if __name__ == "__main__":
    main()
