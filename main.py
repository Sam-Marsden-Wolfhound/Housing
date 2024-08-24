import streamlit as st
import pandas as pd
from dataframe_builder import DataFrameBuilder
from ui import SalaryUI, ExpensesUI, HousingUI
import logging

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)

def main():
    logging.info("Application started")
    # Initialize session state
    if "salary_entries" not in st.session_state:
        st.session_state.salary_entries = []
    if "expense_entries" not in st.session_state:
        st.session_state.expense_entries = []
    if "housing_entries" not in st.session_state:
        st.session_state.housing_entries = []
    if "house_counter" not in st.session_state:  # Ensure house_counter is initialized
        st.session_state.house_counter = 1
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=[
            "Month", "Years", "Salary", "Pension Deductions", "Tax", "National Insurance",
            "Combined Pension Contribution", "Take Home Pay", "Expenses"
        ])

    # Create an instance of DataFrameBuilder
    df_builder = DataFrameBuilder()

    # Sidebar for salary, expenses, and housing with toggle capability
    selected_section = st.sidebar.radio("Select Section", ("Salary", "Expenses", "Housing"))

    if selected_section == "Salary":
        SalaryUI().display(df_builder)
    elif selected_section == "Expenses":
        ExpensesUI().display(df_builder)
    elif selected_section == "Housing":
        HousingUI().display(df_builder)

    # Displaying the DataFrame
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
        df_builder.plot_graph(columns_to_display)
    else:
        st.write("No data available for graphing.")

if __name__ == "__main__":
    main()
