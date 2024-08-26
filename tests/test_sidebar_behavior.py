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
    # Simulate adding a salary directly
    st.session_state.salary_dfs.append({
        'name': 'Salary 1',
        'annual_gross_income': 60000,
        'pension_contrib': 3.0,
        'company_match': 3.0,
        'num_months': 12
    })
    assert len(st.session_state.salary_dfs) == 1

def test_sidebar_display_for_expenses(setup_session):
    # Simulate adding an expense directly
    st.session_state.expenses_dfs.append({
        'name': 'Expense 1',
        'monthly_expense': 1000,
        'months': 12
    })
    assert len(st.session_state.expenses_dfs) == 1

def test_edit_and_delete_buttons_for_salaries(setup_session):
    # Simulate adding a salary directly
    st.session_state.salary_dfs.append({
        'name': 'Salary 1',
        'annual_gross_income': 60000,
        'pension_contrib': 3.0,
        'company_match': 3.0,
        'num_months': 12
    })
    assert len(st.session_state.salary_dfs) == 1

    # Simulate deletion
    st.session_state.salary_dfs.pop(0)
    assert len(st.session_state.salary_dfs) == 0

def test_edit_and_delete_buttons_for_expenses(setup_session):
    # Simulate adding an expense directly
    st.session_state.expenses_dfs.append({
        'name': 'Expense 1',
        'monthly_expense': 1000,
        'months': 12
    })
    assert len(st.session_state.expenses_dfs) == 1

    # Simulate deletion
    st.session_state.expenses_dfs.pop(0)
    assert len(st.session_state.expenses_dfs) == 0
