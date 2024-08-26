import streamlit as st
from ui import SalaryUI, ExpensesUI

def main():
    st.title("Personal Finance Planner")

    tabs = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])

    with tabs[0]:
        ui = SalaryUI()
        ui.display()

    # Placeholder: Implement similar classes for Expenses, Housing, and Analysis.
    with tabs[1]:
        ui = ExpensesUI()
        ui.display()

    with tabs[2]:
        st.header("Housing Management")
        st.write("Housing management content goes here.")

    with tabs[3]:
        st.header("Analysis")
        st.write("Analysis content goes here.")

if __name__ == "__main__":
    main()
