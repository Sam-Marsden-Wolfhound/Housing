import streamlit as st
from ui import SalaryUI, ExpensesUI, HousingUI, StockUI, SavingsUI, AnalysisUI, SessionsUI
from StateManager import StateManager, initialize_state


def main():
    st.title('Finance Planner')
    # st.set_page_config(page_title="Personal Finance Planner", layout="wide")

    # Initialize state manager
    state_manager = StateManager()

    tab = st.tabs([
        'Sessions',
        'Salary',
        'Expenses',
        'Housing',
        'Stocks',
        'Savings',
        'Analysis'
    ])

    with tab[0]:
        ui = SessionsUI(state_manager)
        ui.display()

    with tab[1]:
        ui = SalaryUI(state_manager)
        ui.display()

    with tab[2]:
        ui = ExpensesUI(state_manager)
        ui.display()



    # tab = st.tabs(["Salary", "Expenses", "Housing", "Stocks", "Savings", "Analysis", "Compare", "Sessions"])
    #
    # with tab[0]:
    #     ui = SalaryUI()
    #     ui.display()
    # with tab[1]:
    #     ui = ExpensesUI()
    #     ui.display()
    # with tab[2]:
    #     ui = HousingUI()
    #     ui.display()
    # with tab[3]:
    #     ui = StockUI()
    #     ui.display()
    # with tab[4]:
    #     ui = SavingsUI()
    #     ui.display()
    # with tab[5]:
    #     ui = AnalysisUI()
    #     ui.display()
    # with tab[6]:
    #     st.header("Compare")
    #     # ui = AnalysisUI()
    #     # ui.display()
    # with tab[7]:
    #     ui = SessionsUI()
    #     ui.display()


if __name__ == "__main__":
    main()
