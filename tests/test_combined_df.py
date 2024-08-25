import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
import streamlit as st
from ui import SalaryUI


@pytest.fixture
def setup_salary_ui():
    # Clear session state before each test
    st.session_state.clear()
    ui = SalaryUI()
    return ui


def test_combined_salary_df(setup_salary_ui):
    ui = setup_salary_ui

    # Add multiple salaries and test combined DataFrame
    input_df1, output_df1 = ui.create_salary_df("Salary 1", 60000, 3.0, 3.0, 12)
    input_df2, output_df2 = ui.create_salary_df("Salary 2", 90000, 5.0, 4.0, 12)
    st.session_state.salary_dfs.append({'name': 'Salary 1', 'input_df': input_df1, 'output_df': output_df1})
    st.session_state.salary_dfs.append({'name': 'Salary 2', 'input_df': input_df2, 'output_df': output_df2})

    # Combine and check the combined DataFrame
    combined_df = pd.concat([salary['output_df'] for salary in st.session_state.salary_dfs], ignore_index=True)

    assert combined_df.shape[0] == 24  # 12 months + 12 months
    assert combined_df['Monthly Salary'][0] == 5000
    assert combined_df['Monthly Salary'][12] == 7500
