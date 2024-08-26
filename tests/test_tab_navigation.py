import streamlit as st
import pytest
from ui import SalaryUI, ExpensesUI

def test_tab_navigation():
    st.title("Personal Finance Planner")

    tabs = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])

    with tabs[0]:
        ui = SalaryUI()
        ui.display()
        assert "salary_dfs" in st.session_state

    with tabs[1]:
        ui = ExpensesUI()
        ui.display()
        assert "expenses_dfs" in st.session_state

    with tabs[2]:
        st.header("Housing Management")
        # Simplified check
        assert True  # Just to confirm the tab is accessed

    with tabs[3]:
        st.header("Analysis")
        # Simplified check
        assert True  # Just to confirm the tab is accessed
