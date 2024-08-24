import streamlit as st
from ui import SalaryUI, ExpensesUI, HousingUI
from dataframe_builder import DataFrameBuilder
from financial_entry import FinancialEntry

def main():
    # Initialize session state
    if "df" not in st.session_state:
        # Pass the FinancialEntry instance when creating DataFrameBuilder
        st.session_state.df = DataFrameBuilder(FinancialEntry()).build_empty_dataframe()

    # Create an instance of DataFrameBuilder with FinancialEntry
    df_builder = DataFrameBuilder(FinancialEntry())

    st.title("Personal Financial Dashboard")

    selected_section = st.sidebar.radio("Navigate", ("Salary", "Expenses", "Housing"))

    if selected_section == "Salary":
        SalaryUI().display(df_builder)
    elif selected_section == "Expenses":
        ExpensesUI().display(df_builder)
    elif selected_section == "Housing":
        HousingUI().display(df_builder)

    st.write("### Data Overview")
    st.dataframe(st.session_state.df)

    st.write("### Graphical Analysis")
    columns_to_display = st.multiselect(
        "Select columns to display on the graph",
        options=st.session_state.df.columns,
        default=["Salary", "Take Home Pay", "Expenses"]
    )

    if len(st.session_state.df) > 0 and columns_to_display:
        st.line_chart(st.session_state.df[columns_to_display])

if __name__ == "__main__":
    main()
