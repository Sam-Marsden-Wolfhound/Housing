import streamlit as st
from form_handlers import handle_salary_form, handle_expense_form, handle_housing_form, create_salary_output_df, create_expense_output_df, create_housing_output_df
from sidebar_manager import display_salary_sidebar, display_expense_sidebar, display_housing_sidebar
from data_processing import update_combined_salary_df, update_combined_expenses_df, update_combined_housing_df
from visualizations import display_salary_graph, display_expenses_graph, display_housing_graph

class SalaryUI:
    def display(self):
        st.header("Salary Management")
        with st.form(key='salary_form'):
            if handle_salary_form():
                update_combined_salary_df()
        display_salary_sidebar(create_salary_output_df, update_combined_salary_df)
        st.subheader("Combined Salary DataFrame")
        st.dataframe(st.session_state.combined_salary_df)
        display_salary_graph()

class ExpensesUI:
    def display(self):
        st.header("Expense Management")
        with st.form(key='expense_form'):
            if handle_expense_form():
                update_combined_expenses_df()
        display_expense_sidebar(create_expense_output_df, update_combined_expenses_df)
        st.subheader("Combined Expense DataFrame")
        st.dataframe(st.session_state.combined_expenses_df)
        display_expenses_graph()

class HousingUI:
    def display(self):
        st.header("Housing Management")
        with st.form(key='housing_form'):
            if handle_housing_form():
                update_combined_housing_df()
        display_housing_sidebar(create_housing_output_df, update_combined_housing_df)
        st.subheader("Combined Housing DataFrame")
        st.dataframe(st.session_state.combined_housing_df)
        display_housing_graph()



