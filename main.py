import streamlit as st
from financial_entry import FinancialEntry
from dataframe_builder import DataFrameBuilder
from ui import SalaryUI, ExpensesUI, HousingUI, AnalysisUI


def main():
    st.set_page_config(page_title="Financial Planner", layout="wide")
    if "financial_entry" not in st.session_state:
        st.session_state.financial_entry = FinancialEntry()

    df_builder = DataFrameBuilder(st.session_state.financial_entry)

    tabs = ["Salary", "Expenses", "Housing", "Analysis"]
    selected_tab = st.sidebar.radio("Select a Tab", tabs)

    if selected_tab == "Salary":
        SalaryUI().display(df_builder)
    elif selected_tab == "Expenses":
        ExpensesUI().display(df_builder)
    elif selected_tab == "Housing":
        HousingUI().display(df_builder)
    elif selected_tab == "Analysis":
        AnalysisUI().display(df_builder)


if __name__ == "__main__":
    main()
