import streamlit as st
from dataframe_builder import DataFrameBuilder
from financial_entry import FinancialEntry
from ui import SalaryUI, ExpensesUI, HousingUI


def main():
    st.set_page_config(page_title="Personal Finance App", layout="wide")

    # Initialize the financial entry and DataFrame builder
    financial_entry = FinancialEntry()
    df_builder = DataFrameBuilder(financial_entry)

    # Initial empty DataFrame
    if "df" not in st.session_state:
        st.session_state.df = df_builder.build_empty_dataframe()

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
        st.line_chart(st.session_state.df.set_index("Month")[columns_to_display])
    else:
        st.write("No data available for graphing.")


if __name__ == "__main__":
    main()
