import streamlit as st
from ui import SalaryUI, ExpensesUI, HousingUI, StockUI, SavingsUI
from state_manager import initialize_state


def main():
    initialize_state()

    st.title("Personal Finance Planner")

    tab = st.tabs(["Salary", "Expenses", "Housing", "Stocks", "Savings", "Analysis"])

    with tab[0]:
        ui = SalaryUI()
        ui.display()
    with tab[1]:
        ui = ExpensesUI()
        ui.display()
    with tab[2]:
        ui = HousingUI()
        ui.display()
    with tab[3]:
        ui = StockUI()
        ui.display()
    with tab[4]:
        ui = SavingsUI()
        ui.display()
    with tab[5]:
        st.subheader("Analysis Tab")


if __name__ == "__main__":
    main()
