import streamlit as st
from ui import SalaryUI, ExpensesUI, HousingUI, StockUI, AssetUI, AnalysisUI, SessionsUI, CompareSessionsUI
from StateManager import StateManager
from sidebar_manager import display_refresh_sidebar_button


def main():
    # st.title('Finance Planner')
    st.set_page_config(page_title="Finance Planner", layout="wide")

    # Initialize state manager
    state_manager = StateManager()

    tab = st.tabs([
        'Sessions',
        'Salary',
        'Expenses',
        'Housing',
        'Stocks',
        'Assets',
        'Analysis',
        'Compare_Sessions',
    ])
    display_refresh_sidebar_button(state_manager)  # Add the Refresh Sidebar button at the top with a unique key
    # refresh_sidebar(self.state_manager)

    with tab[0]:
        ui = SessionsUI(state_manager)
        ui.display()

    with tab[1]:
        ui = SalaryUI(state_manager)
        ui.display()

    with tab[2]:
        ui = ExpensesUI(state_manager)
        ui.display()

    with tab[3]:
        ui = HousingUI(state_manager)
        ui.display()

    with tab[4]:
        ui = StockUI(state_manager)
        ui.display()

    with tab[5]:
        ui = AssetUI(state_manager)
        ui.display()

    # with tab[6]:
    #     st.header("Compare")
    #     # ui = AnalysisUI()
    #     # ui.display()

    with tab[6]:
        ui = AnalysisUI(state_manager)
        ui.display()

    with tab[7]:
        ui = CompareSessionsUI(state_manager)
        ui.display()


if __name__ == "__main__":
    main()
