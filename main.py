import streamlit as st
import pandas as pd
from financial_entry import FinancialEntry
from dataframe_builder import DataFrameBuilder
from ui import SalaryUI, ExpensesUI, HousingUI, AnalysisUI

def main():
    st.set_page_config(layout="wide")

    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame()

    df_builder = DataFrameBuilder(FinancialEntry())

    tab1, tab2, tab3, tab4 = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])

    with tab1:
        SalaryUI().display(df_builder)

    with tab2:
        ExpensesUI().display(df_builder)

    with tab3:
        HousingUI().display(df_builder)

    with tab4:
        AnalysisUI().display(df_builder)

    st.session_state.df.set_index("Month", inplace=True)

if __name__ == "__main__":
    main()
