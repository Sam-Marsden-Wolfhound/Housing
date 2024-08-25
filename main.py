import streamlit as st
from ui import UI
from dataframe_builder import DataFrameBuilder
from financial_entry import FinancialEntry

def main():
    df_builder = DataFrameBuilder(FinancialEntry())
    UI().display(df_builder)

if __name__ == "__main__":
    main()
