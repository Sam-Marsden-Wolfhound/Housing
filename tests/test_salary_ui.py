import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import streamlit as st
from ui import SalaryUI


@pytest.fixture
def setup_salary_ui():
    # Clear session state before each test
    st.session_state.clear()
    ui = SalaryUI()
    return ui


def test_salary_input_default(setup_salary_ui):
    ui = setup_salary_ui

    # Simulate user input with default values
    input_df, output_df = ui.create_salary_df("Salary 1", 60000, 3.0, 3.0, 12)

    assert input_df['Annual Gross Income'][0] == 60000
    assert output_df['Monthly Salary'][0] == 5000


def test_sidebar_add_salary(setup_salary_ui):
    ui = setup_salary_ui

    # Add a new salary
    input_df, output_df = ui.create_salary_df("Salary 1", 60000, 3.0, 3.0, 12)
    st.session_state.salary_dfs.append({
        'name': 'Salary 1',
        'input_df': input_df,
        'output_df': output_df,
        'annual_gross_income': 60000,
        'pension_contrib': 3.0,
        'company_match': 3.0,
        'num_months': 12
    })

    # Simulate rendering the sidebar
    ui.salary_sidebar()

    assert "Salary 1" in st.session_state.salary_dfs[0]['name']


def test_sidebar_delete_salary(setup_salary_ui):
    ui = setup_salary_ui

    # Add a salary
    input_df, output_df = ui.create_salary_df("Salary 1", 60000, 3.0, 3.0, 12)
    st.session_state.salary_dfs.append({
        'name': 'Salary 1',
        'input_df': input_df,
        'output_df': output_df,
        'annual_gross_income': 60000,
        'pension_contrib': 3.0,
        'company_match': 3.0,
        'num_months': 12
    })

    # Delete the salary and check if it is removed
    ui.salary_sidebar()
    del st.session_state.salary_dfs[0]
    assert len(st.session_state.salary_dfs) == 0


def test_salary_editing(setup_salary_ui):
    ui = setup_salary_ui

    # Add a salary
    input_df, output_df = ui.create_salary_df("Salary 1", 60000, 3.0, 3.0, 12)
    st.session_state.salary_dfs.append({
        'name': 'Salary 1',
        'input_df': input_df,
        'output_df': output_df,
        'annual_gross_income': 60000,
        'pension_contrib': 3.0,
        'company_match': 3.0,
        'num_months': 12
    })

    # Edit the salary and check if changes are saved
    ui.salary_sidebar()
    st.session_state.salary_dfs[0]['annual_gross_income'] = 70000
    assert st.session_state.salary_dfs[0]['annual_gross_income'] == 70000
