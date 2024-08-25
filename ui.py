import streamlit as st
from dataframe_builder import DataFrameBuilder

class UI:
    def display(self, df_builder: DataFrameBuilder):
        tab1, tab2, tab3, tab4 = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])

        with tab1:
            SalaryUI().display(df_builder)
        with tab2:
            ExpensesUI().display(df_builder)
        with tab3:
            HousingUI().display(df_builder)
        with tab4:
            AnalysisUI().display(df_builder)

class SalaryUI:
    def display(self, df_builder: DataFrameBuilder):
        st.write("Salary UI")

class ExpensesUI:
    def display(self, df_builder: DataFrameBuilder):
        st.write("Expenses UI")

class HousingUI:
    def display(self, df_builder: DataFrameBuilder):
        st.write("Housing UI")

class AnalysisUI:
    def display(self, df_builder: DataFrameBuilder):
        st.write("Analysis UI")
