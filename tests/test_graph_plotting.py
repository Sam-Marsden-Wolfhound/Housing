import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import streamlit as st
import pandas as pd
from ui import SalaryUI


@pytest.fixture
def setup_salary_ui():
    # Clear session state before each test
    st.session_state.clear()
    ui = SalaryUI()
    return ui


def test_graph_default_selection(setup_salary_ui):
    ui = setup_salary_ui

    # Add a salary
    input_df, output_df = ui.create_salary_df("Salary 1", 60000, 3.0, 3.0, 12)
    st.session_state.salary_dfs.append({'name': 'Salary 1', 'input_df': input_df, 'output_df': output_df})

    # Mock the Streamlit selection and plot the graph
    columns_to_plot = ["Monthly Salary"]
    combined_df = pd.concat([salary['output_df'] for salary in st.session_state.salary_dfs], ignore_index=True)

    # Test if "Monthly Salary" is selected and plotted by default
    assert "Monthly Salary" in combined_df.columns
    assert combined_df['Monthly Salary'].iloc[0] == 5000


def test_graph_sequential_plotting(setup_salary_ui):
    ui = setup_salary_ui

    # Add two salaries
    input_df1, output_df1 = ui.create_salary_df("Salary 1", 60000, 3.0, 3.0, 12)
    input_df2, output_df2 = ui.create_salary_df("Salary 2", 90000, 5.0, 4.0, 12)
    st.session_state.salary_dfs.append({'name': 'Salary 1', 'input_df': input_df1, 'output_df': output_df1})
    st.session_state.salary_dfs.append({'name': 'Salary 2', 'input_df': input_df2, 'output_df': output_df2})

    # Combine and plot sequentially
    combined_df = pd.concat([salary['output_df'] for salary in st.session_state.salary_dfs], ignore_index=True)

    # Ensure the plot is sequential
    assert combined_df['Monthly Salary'].iloc[0] == 5000
    assert combined_df['Monthly Salary'].iloc[12] == 7500
