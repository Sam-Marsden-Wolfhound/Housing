import streamlit as st

def display_salary_sidebar(update_combined_df):
    st.sidebar.header("Your Salaries")
    for i, salary_data in enumerate(st.session_state.salary_dfs):
        with st.sidebar.expander(salary_data['name'], expanded=False):
            display_salary_details(i, salary_data, update_combined_df)

def display_expense_sidebar(update_combined_df):
    st.sidebar.header("Your Expenses")
    for i, expense_data in enumerate(st.session_state.expenses_dfs):
        with st.sidebar.expander(expense_data['name'], expanded=False):
            display_expense_details(i, expense_data, update_combined_df)

def display_salary_details(i, salary_data, update_combined_df):
    if st.button("Edit", key=f"edit_salary_{i}"):
        st.session_state.editing_salary_index = i
    if st.button("Delete", key=f"delete_salary_{i}"):
        del st.session_state.salary_dfs[i]
        update_combined_df()
        st.experimental_rerun()

def display_expense_details(i, expense_data, update_combined_df):
    if st.button("Edit", key=f"edit_expense_{i}"):
        st.session_state.editing_expense_index = i
    if st.button("Delete", key=f"delete_expense_{i}"):
        del st.session_state.expenses_dfs[i]
        update_combined_df()
        st.experimental_rerun()
