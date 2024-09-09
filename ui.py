import streamlit as st
import pandas as pd
import os
from form_handlers import handle_salary_form, handle_rent_form, handle_expense_form, handle_house_form, handle_stock_form, handle_asset_form, create_salary_output_df, create_expense_output_df, create_house_output_df, create_rent_output_df, create_stock_output_df, create_asset_output_df
from sidebar_manager import display_salary_sidebar, display_expense_sidebar, display_housing_sidebar, display_rent_sidebar, display_stock_sidebar, display_asset_sidebar
from data_processing import update_combined_salary_df, update_combined_expenses_df, update_combined_housing_df, update_combined_rent_df, update_combined_housing_and_rent_df, update_combined_stock_df, update_combined_asset_df, update_combined_analysis_df

from visualizations import display_graph, display_expenses_graph, display_housing_and_rent_graph, display_stock_graph, display_savings_graph, display_analysis_graph

from StateManager import save_session_state, update_session_state, load_session_state


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
            session_files = [f for f in os.listdir(directory) if f.startswith("Session_") and f.endswith(".pkl")]
            selected_file = st.selectbox("Select a session to load:", session_files, key="select_session")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("Load Session", key="loud_session"):
                    if selected_file:
                        print("louding button", selected_file)
                        file_path = os.path.join(directory, selected_file)
                        load_session_state(self.state_manager, file_path)

            with col2:
                if st.button("Update Session", key="update_session"):
                    update_session_state(self.state_manager, directory, selected_file)

    def display(self):
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
        st.header("Salary Management")
        with st.form(key='salary_form'):
            if handle_salary_form(self.state_manager):
                self.state_manager.update_all()

        display_salary_sidebar(self.state_manager)

        st.subheader("Combined Salary DataFrame")
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
                             'Take Home Pay'
            ]
        )

class ExpensesUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        st.header("Expense Management")
        with st.form(key='expense_form'):
            if handle_expense_form(self.state_manager):
                self.state_manager.update_all()
        display_expense_sidebar(self.state_manager)

        st.subheader("Combined Expense DataFrame")

        # st.dataframe(st.session_state.combined_expenses_df)
        # display_expenses_graph()

class HousingUI:
    def display(self):
        st.header("Housing Management")
        with st.form(key='housing_form'):
            if handle_housing_form():
                update_combined_housing_df()
                update_combined_housing_and_rent_df()

        display_housing_sidebar(create_housing_output_df, update_combined_housing_df, update_combined_housing_and_rent_df)

        with st.expander("Combined Housing DataFrame", expanded=False):
            st.dataframe(st.session_state.combined_housing_df)

        st.header("Rent Management")
        with st.form(key='rent_form'):
            if handle_rent_form():
                update_combined_rent_df()
                update_combined_housing_and_rent_df()

        display_rent_sidebar(create_rent_output_df, update_combined_rent_df, update_combined_housing_and_rent_df)

        with st.expander("Combined Rent DataFrame", expanded=False):
            st.dataframe(st.session_state.combined_rent_df)

        st.subheader("Housing & Rent DataFrame")
        st.dataframe(st.session_state.combined_housing_and_rent_df)

        display_housing_and_rent_graph()

class StockUI:
    def display(self):
        st.header("Stock Management")
        with st.form(key='stock_form'):
            if handle_stock_form():
                update_combined_stock_df()
                pass
        st.subheader("Combined Stock DataFrame")
        # cb_housing_df_timeframe = st.number_input("Time Frame", value=40)
        display_stock_sidebar(create_stock_output_df, update_combined_stock_df)
        st.dataframe(st.session_state.combined_stock_df)
        display_stock_graph()

class SavingsUI:
    def display(self):
        st.header("Savings Management")
        with st.form(key='savings_form'):
            if handle_asset_form():
                update_combined_savings_df()

        st.subheader("Combined Savings DataFrame")
        display_asset_sidebar(create_savings_output_df, update_combined_savings_df)
        st.dataframe(st.session_state.combined_savings_df)
        display_savings_graph()

class AnalysisUI:
    def display(self):
        st.header("Analysis")
        if st.button("Refresh Page", key="refresh_analysis"):
            update_combined_analysis_df()

        with st.form(key='Analysis_form'):
            pass

        st.subheader("Analysis_Combined DataFrame")
        st.dataframe(st.session_state.combined_analysis_df)

        # Add download button to download the combined analysis DataFrame as a CSV
        csv = st.session_state.combined_analysis_df.to_csv(index=False)
        st.download_button(
            label="Download DataFrame",
            data=csv,
            file_name='combined_analysis.csv',
            mime='text/csv'
        )
        display_analysis_graph()





