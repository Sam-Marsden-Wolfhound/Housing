import logging
import streamlit as st
from ui import SalaryUI, ExpensesUI, HousingUI, AnalysisUI
from dataframe_builder import DataFrameBuilder
from financial_entry import FinancialEntry

logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    st.set_page_config(layout="wide")
    logging.info("Application started.")

    if "df" not in st.session_state:
        st.session_state.df = DataFrameBuilder(FinancialEntry()).build_empty_dataframe()

    st.title("Financial Planning Tool")

    tabs = ["Salary", "Expenses", "Housing", "Analysis"]
    selected_tab = st.selectbox("Select a tab", tabs)

    df_builder = DataFrameBuilder(FinancialEntry())

    if selected_tab == "Salary":
        SalaryUI().display(df_builder)
    elif selected_tab == "Expenses":
        ExpensesUI().display(df_builder)
    elif selected_tab == "Housing":
        HousingUI().display(df_builder)
    elif selected_tab == "Analysis":
        AnalysisUI().display(df_builder)

    st.session_state.df.set_index("Month", inplace=True)
    logging.info("Application finished.")

if __name__ == "__main__":
    main()
