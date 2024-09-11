import streamlit as st
import pandas as pd
import os
from StateManager import save_session_state, update_session_state, load_session_state
from form_handlers import handle_salary_form, handle_rent_form, handle_expense_form, handle_house_form, handle_stock_form, handle_asset_form, create_salary_output_df, create_expense_output_df, create_house_output_df, create_rent_output_df, create_stock_output_df, create_asset_output_df
from sidebar_manager import display_salary_sidebar, display_expense_sidebar, display_house_sidebar, display_rent_sidebar, display_stock_sidebar, display_asset_sidebar
from visualizations import display_graph



class SessionsUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display_save_section(self, directory):
        with st.container(border=True):
            st.subheader("New Save")
            filename = st.text_input("File Name", value="Finances", key="filename_save")
            col1, col2 = st.columns(2)
            with col2:
                # Add UUID to file name
                use_uuid = st.checkbox("Add Session UUID", value=True, key="check_box_uuid")

            with col1:
                # Save Session
                if st.button("Save Session", key="save_session"):
                    save_session_state(self.state_manager, directory, filename, use_uuid)

    def display_load_section(self, directory):
        with st.container(border=True):
            st.subheader("Load & Update")
            # Get sessions in directory
            # session_files = [f for f in os.listdir(directory) if f.startswith("Session_") and f.endswith(".pkl")]
            session_files = [f for f in os.listdir(directory) if f.endswith(".pkl")]

            selected_file = st.selectbox("Select a session to load:", session_files, key="select_session")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Load Session", key="loud_session"):
                    if selected_file:
                        print("louding button", selected_file)
                        file_path = os.path.join(directory, selected_file)
                        load_session_state(self.state_manager, file_path)
                        self.state_manager.update_all()

            with col2:
                if st.button("Update Session", key="update_session"):
                    update_session_state(self.state_manager, directory, selected_file)

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Sessions")
            # Input for directory
            directory = st.text_input(
                "Target Session Directory",
                value="Saved_Sessions",
                key="directory_save"
            )

            self.display_save_section(directory)
            self.display_load_section(directory)


class SalaryUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Salary Management")
            with st.form(key='salary_form'):
                if handle_salary_form(self.state_manager):
                    self.state_manager.update_all()

        display_salary_sidebar(self.state_manager)

        with st.expander("Combined Salary DataFrame", expanded=False):
            # st.subheader("Combined Salary DataFrame")
            #
            # pension_groth = st.number_input("Pension Groth", value=st.session_state.pension_groth)
            # if st.button("Update Pension Groth", key="update_pension_groth"):
            #     st.session_state['pension_groth'] = pension_groth
            #     update_combined_salary_df()
            #
            st.dataframe(self.state_manager.get_combined_salary_df())

        display_graph(
            title='Salary Graph',
            dataframe=self.state_manager.get_combined_salary_df(),
            default_columns=['Monthly Salary',
                             'Take Home Pay',
                             'Combined Pension Contribution'
            ]
        )

class ExpensesUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Expense Management")
            with st.form(key='expense_form'):
                if handle_expense_form(self.state_manager):
                    self.state_manager.update_all()

        display_expense_sidebar(self.state_manager)

        with st.expander("Combined Expense DataFrame", expanded=False):
            # st.subheader("Combined Expense DataFrame")
            st.dataframe(self.state_manager.get_combined_expense_df())

        display_graph(
            title='Expenses Graph',
            dataframe=self.state_manager.get_combined_expense_df(),
            default_columns=['Monthly Expenses'
                             ]
        )


class HousingUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Housing Management")
            with st.form(key='housing_form'):
                if handle_house_form(self.state_manager):
                    self.state_manager.update_all()

            display_house_sidebar(self.state_manager)

            st.header("Rent Management")
            with st.form(key='rent_form'):
                if handle_rent_form(self.state_manager):
                    self.state_manager.update_all()

        display_rent_sidebar(self.state_manager)

        with st.expander("Combined Housing DataFrame", expanded=False):
            st.dataframe(self.state_manager.get_combined_house_df())

        with st.expander("Combined Rent DataFrame", expanded=False):
            st.dataframe(self.state_manager.get_combined_rent_df())

        with st.expander("Housing & Rent DataFrame", expanded=False):
            # st.subheader("Housing & Rent DataFrame")
            st.dataframe(self.state_manager.get_combined_house_and_rent_df())

        display_graph(
            title='Housing & Rent Graph',
            dataframe=self.state_manager.get_combined_house_and_rent_df(),
            default_columns=['Row Total Payment Amount',
                             'Row Total Interest Amount',
                             'Row Total Rent Amount'
                             ]
        )


class StockUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Stock Management")
            with st.form(key='stock_form'):
                if handle_stock_form(self.state_manager):
                    self.state_manager.update_all()

        display_stock_sidebar(self.state_manager)

        with st.expander("Combined Stock DataFrame", expanded=False):
            # st.subheader("Combined Stock DataFrame")
            st.dataframe(self.state_manager.get_combined_stock_df())

        display_graph(
            title='Stock Graph',
            dataframe=self.state_manager.get_combined_stock_df(),
            default_columns=['Running Total Investment Amount',
                             'Running Total Cash Value',
                             'Running Total Cashout Amount Stocks',
                             'Delta',
                             ]
        )

class AssetUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.header("Asset Management")
            with st.form(key='asset_form'):
                if handle_asset_form(self.state_manager):
                    self.state_manager.update_all()

        display_asset_sidebar(self.state_manager)

        with st.expander("Combined Asset DataFrame", expanded=False):
            # st.subheader("Combined Asset DataFrame")
            st.dataframe(self.state_manager.get_combined_asset_df())
        display_graph(
            title='Asset Graph',
            dataframe=self.state_manager.get_combined_asset_df(),
            default_columns=['Row Total Asset Value',
                             ]
        )

class AnalysisUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        st.header("Analysis")

        # col1, col2 = st.columns(2)
        # with col1:
        #     st.header("Analysis")
        # with col2:
        #     if st.button("Refresh Page", key="refresh_analysis"):
        #         self.state_manager.update_all()

        with st.expander("Analysis_Combined DataFrame", expanded=False):
            # st.subheader("Analysis_Combined DataFrame")
            st.dataframe(self.state_manager.get_combined_analysis_df())

            # Add download button to download the combined analysis DataFrame as a CSV
            csv = self.state_manager.get_combined_analysis_df().to_csv(index=False)
            st.download_button(
                label="Download DataFrame",
                data=csv,
                file_name='combined_analysis.csv',
                mime='text/csv'
            )
        display_graph(
            title='Analysis Graph - Monthly Brickdown',
            dataframe=self.state_manager.get_combined_analysis_df(),  # XX
            default_columns=['Monthly Cash Savings',
                             'Monthly Credit',
                             'Monthly Investment',
                             'Monthly Losses'
                             ]
        )

        display_graph(
            title='Analysis Graph - Running Total',
            dataframe=self.state_manager.get_combined_analysis_df(),  # XX
            default_columns=['Running Total Cash Savings',
                             'Running Total Asset Amount',
                             'Running Total Cash & Asset',
                             'Running Total Cash & Asset & Pension'
                             ]
        )



