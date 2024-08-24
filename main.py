import streamlit as st
import pandas as pd
import logging
from ui import SalaryUI, ExpensesUI, HousingUI
from dataframe_builder import DataFrameBuilder
from financial_entry import FinancialEntry

# Configure logging
logging.basicConfig(filename="app.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    logging.info("App started")

    # Initialize session state
    if "salary_entries" not in st.session_state:
        st.session_state.salary_entries = []
    if "expense_entries" not in st.session_state:
        st.session_state.expense_entries = []
    if "housing_entries" not in st.session_state:
        st.session_state.housing_entries = []
    if "house_counter" not in st.session_state:
        st.session_state.house_counter = 1
    if "df" not in st.session_state:
        st.session_state.df = pd.DataFrame(columns=[
            "Month", "Years", "Salary", "Pension Deductions", "Tax", "National Insurance",
            "Combined Pension Contribution", "Take Home Pay", "Expenses"
        ])

    # Create instances of UI classes
    df_builder = DataFrameBuilder(FinancialEntry())

    # Render the UI sections
    selected_section = st.sidebar.radio("Select Section", ("Salary", "Expenses", "Housing"))

    if selected_section == "Salary":
        SalaryUI().display(df_builder)
    elif selected_section == "Expenses":
        ExpensesUI().display(df_builder)
    elif selected_section == "Housing":
        HousingUI().display(df_builder)

    # Display the DataFrame
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
        plt.figure(figsize=(10, 6))

        for column in columns_to_display:
            plt.plot(st.session_state.df.index, st.session_state.df[column], label=column)

        plt.xlabel("Month")
        plt.ylabel("Amount (£)")
        plt.title("Monthly Financial Breakdown")
        plt.legend()
        st.pyplot(plt)
    else:
        st.write("No data available for graphing.")

    logging.info("App finished execution")


if __name__ == "__main__":
    main()
