import streamlit as st
import pytest
from ui import SalaryUI, ExpensesUI

def test_tab_navigation():
    st.title("Personal Finance Planner")

    tabs = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])

    with tabs[0]:
        ui = SalaryUI()
        ui.display()
        assert "Add New Salary" in st.session_state

    with tabs[1]:
        ui = ExpensesUI()
        ui.display()
        assert "Add New Expense" in st.session_state

    with tabs[2]:
        assert "Housing Management" in st.session_state

    with tabs[3]:
        assert "Analysis" in st.session_state
