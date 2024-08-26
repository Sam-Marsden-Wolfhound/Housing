import streamlit as st
from form_handlers import handle_salary_form, handle_expense_form
from sidebar_manager import display_salary_sidebar, display_expense_sidebar
from data_processing import update_combined_salary_df, update_combined_expenses_df
from visualizations import display_salary_graph, display_expenses_graph

class SalaryUI:
    def display(self):
        st.header("Salary Management")
        with st.form(key='salary_form'):
            if handle_salary_form():
                update_combined_salary_df()
        display_salary_sidebar(update_combined_salary_df)
        st.dataframe(st.session_state.combined_salary_df)
        display_salary_graph()

class ExpensesUI:
    def display(self):
        st.header("Expense Management")
        with st.form(key='expense_form'):
            if handle_expense_form():
                update_combined_expenses_df()
        display_expense_sidebar(update_combined_expenses_df)
        st.dataframe(st.session_state.combined_expenses_df)
        display_expenses_graph()
