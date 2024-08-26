import streamlit as st
import pytest
from ui import SalaryUI, ExpensesUI

@pytest.fixture
def setup_session():
    st.session_state.clear()
    st.session_state['salary_dfs'] = []
    st.session_state['expenses_dfs'] = []
    st.session_state['next_salary_id'] = 1
    st.session_state['next_expense_id'] = 1

def test_sidebar_display_for_salary(setup_session):
    ui = SalaryUI()
    ui.display()

    # Test the existence of the "Refresh Sidebar" button
    assert "Refresh Sidebar" in st.sidebar
    # Ensure that salaries list is empty initially
    assert len(st.session_state.salary_dfs) == 0

    # Add a salary and check the sidebar
    ui.salary_input_form()
    assert len(st.session_state.salary_dfs) == 1

def test_sidebar_display_for_expenses(setup_session):
    ui = ExpensesUI()
    ui.display()

    # Test the existence of the "Refresh Sidebar" button
    assert "Refresh Sidebar" in st.sidebar
    # Ensure that expenses list is empty initially
    assert len(st.session_state.expenses_dfs) == 0

    # Add an expense and check the sidebar
    ui.expenses_input_form()
    assert len(st.session_state.expenses_dfs) == 1

def test_edit_and_delete_buttons_for_salaries(setup_session):
    ui = SalaryUI()
    ui.display()

    # Add a salary
    ui.salary_input_form()
    assert len(st.session_state.salary_dfs) == 1

    # Test the delete button
    ui.salary_sidebar()
    st.sidebar.button("Delete Salary 1")
    assert len(st.session_state.salary_dfs) == 0

def test_edit_and_delete_buttons_for_expenses(setup_session):
    ui = ExpensesUI()
    ui.display()

    # Add an expense
    ui.expenses_input_form()
    assert len(st.session_state.expenses_dfs) == 1

    # Test the delete button
    ui.expenses_sidebar()
    st.sidebar.button("Delete Expense 1")
    assert len(st.session_state.expenses_dfs) == 0
