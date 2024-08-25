import streamlit as st
from ui import SalaryUI, ExpensesUI, HousingUI
from dataframe_builder import DataFrameBuilder
from financial_entry import FinancialEntry

""" Need to reset the code based on this files"""

def main():
    st.title("Housing and Financial Planner")

    if "df" not in st.session_state:
        st.session_state.df = DataFrameBuilder(FinancialEntry()).rebuild_dataframe()

    df_builder = DataFrameBuilder(FinancialEntry())

    # Tabs for different sections of the app
    tabs = st.tabs(["Salary", "Expenses", "Housing", "View Data"])

    with tabs[0]:
        SalaryUI().display(df_builder)
    with tabs[1]:
        ExpensesUI().display(df_builder)
    with tabs[2]:
        HousingUI().display(df_builder)
    with tabs[3]:
        st.write(st.session_state.df)

    # Set the DataFrame's index to "Month" if it's not already
    if "Month" in st.session_state.df.columns:
        st.session_state.df.set_index("Month", inplace=True)

if __name__ == "__main__":
    main()
