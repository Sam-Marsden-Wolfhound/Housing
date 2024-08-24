import streamlit as st
from dataframe_builder import DataFrameBuilder
from ui import SalaryUI, ExpenseUI, HousingUI

# Initialize the Streamlit app
def main():
    st.title("Financial Overview Application")

    selected_section = st.sidebar.radio("Select Section", ("Salary", "Expenses", "Housing"))

    df_builder = DataFrameBuilder()

    if selected_section == "Salary":
        SalaryUI().display(df_builder)

    elif selected_section == "Expenses":
        ExpenseUI().display(df_builder)

    elif selected_section == "Housing":
        HousingUI().display(df_builder)

    # Display the DataFrame and Graph
    st.write("### Monthly Financial Overview")
    st.write(df_builder.get_dataframe())

    columns_to_display = st.multiselect(
        "Select columns to display on the graph",
        options=df_builder.get_dataframe().columns,
        default=["Salary", "Take Home Pay", "Expenses"]
    )

    st.write("### Monthly Breakdown Graph")
    df_builder.plot_graph(columns_to_display)

if __name__ == "__main__":
    main()
