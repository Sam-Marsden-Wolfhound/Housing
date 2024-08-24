import streamlit as st
import pandas as pd
from ui import SalaryUI, ExpensesUI, HousingUI
from dataframe_builder import DataFrameBuilder

def main():
    # Initialize the DataFrame builder
    df_builder = DataFrameBuilder()

    # UI Sections
    st.sidebar.title("Financial Overview")
    section = st.sidebar.radio("Go to", ["Salary", "Expenses", "Housing"])

    if section == "Salary":
        SalaryUI().display(df_builder)
    elif section == "Expenses":
        ExpensesUI().display(df_builder)
    elif section == "Housing":
        HousingUI().display(df_builder)

    # Display the DataFrame
    if "df" in st.session_state:
        st.write("### Monthly Financial Overview")
        st.write(st.session_state.df)

        # Selecting columns to display on the graph
        columns_to_display = st.multiselect(
            "Select columns to display on the graph",
            options=st.session_state.df.columns,
            default=["Salary", "Take Home Pay", "Expenses"]
        )

        # Plotting the results
        st.write("### Monthly Breakdown Graph")
        if len(st.session_state.df) > 0:
            st.line_chart(st.session_state.df[columns_to_display])
        else:
            st.write("No data available for graphing.")

if __name__ == "__main__":
    main()
