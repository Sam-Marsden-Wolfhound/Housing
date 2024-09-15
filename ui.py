import streamlit as st
import os
from StateManager import save_session_state, update_session_state, load_session_state, new_session_state, delete_session, get_session_json_from_file
from form_handlers import handle_user_form, handle_salary_form, handle_pension_growth_form, handle_rent_form, handle_expense_form, handle_house_form, handle_stock_form, handle_asset_form
from sidebar_manager import display_salary_sidebar, display_pension_sidebar, display_expense_sidebar, display_house_sidebar, display_rent_sidebar, display_stock_sidebar, display_asset_sidebar
from visualizations import display_graph_plotly, display_graph_overview
from util import clean_directory_list, get_index_of_value_in_list

def set_header_and_refresh_button(header, update_handlers):
    col1, col2 = st.columns([3.9, 1])
    with col1:
        st.header(header)
    with col2:
        key = header.split(' ')[0]
        if st.button("Refresh Page", key=f'refresh_{key}_button'):
            for update_handler in update_handlers:
                update_handler()

class SessionsUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display_save_section(self, directory):
        with st.container(border=True):
            st.subheader("New Save")
            filename = st.text_input("File Name", value="Finances", key="filename_save")

            col1, col2 = st.columns([1, 1])
            message_placeholder = st.empty()

            with col2:
                # Add UUID to file name
                use_uuid = st.checkbox("Add Session UUID", value=False, key="check_box_uuid")

            with col1:
                # Save Session
                if st.button("Save Session", key="save_session"):
                    save_session_state(self.state_manager, directory, filename, use_uuid, message_placeholder)

    def display_load_section(self, directory):
        # CSS to style the delete button
        # delete_button_css = """
        #     <style>
        #     .delete-button {
        #         background-color: rgba(255, 0, 0, 0.7);
        #         color: white;
        #         padding: 0.5rem 1rem;
        #         font-size: 1rem;
        #         border-radius: 5px;
        #         border: none;
        #         cursor: pointer;
        #     }
        #     .delete-button:hover {
        #         background-color: darkred;
        #     }
        #     </style>
        # """

        # Inject the custom CSS to Streamlit
        # st.markdown(delete_button_css, unsafe_allow_html=True)

        with st.container(border=True):
            st.subheader("Load & Update")
            # Get sessions in directory
            # session_files = [f for f in os.listdir(directory) if f.startswith("Session_") and f.endswith(".pkl")]
            session_files = [f for f in os.listdir(directory) if f.endswith(".json")]

            selected_file = st.selectbox("Select a session to load:", session_files, key="select_session")

            col1, col2, col3, col4 = st.columns([0.9, 1, 0.85, 1])
            # Create a placeholder for the success message outside the columns
            message_placeholder = st.empty()

            with col1:
                if st.button("Load Session", key="loud_session"):
                    if selected_file:
                        load_session_state(self.state_manager, directory, selected_file, message_placeholder)
                        self.state_manager.update_all()

            with col2:
                if st.button("Update Session", key="update_session"):
                    update_session_state(self.state_manager, directory, selected_file, message_placeholder)

            with col3:
                if st.button("New Session", key="new_session"):
                    new_session_state(self.state_manager)

            with col4:
                # Use st.markdown to display the custom-styled button
                # if st.markdown('<button class="delete-button">Delete Session</button>', unsafe_allow_html=True):
                if st.button("Delete Session", key="delete_session"):
                    delete_session(directory, selected_file, message_placeholder)


    def diplay_user_section(self):
        st.header("User")
        with st.form(key='user_form'):
            if handle_user_form(self.state_manager):
                self.state_manager.update_all()


    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            self.diplay_user_section()

            st.header('Sessions')
            # Check if the file exists and delete it before writing the new one
            if not os.path.exists('saved_sessions'):
                os.makedirs('saved_sessions')
            # # Input for directory
            # directory = st.text_input(
            #     "Target Session Directory",
            #     value="Saved_Sessions",
            #     key="directory_save"
            # )
            directorys = [f for f in os.listdir() if os.path.isdir(f)]
            directorys = clean_directory_list(directorys)
            default_index = get_index_of_value_in_list(directorys, 'saved_sessions')
            selected_directory = st.selectbox('Select a directory to load from:', directorys, key='select_directory', index=default_index)

            self.display_save_section(selected_directory)
            self.display_load_section(selected_directory)


class SalaryUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            set_header_and_refresh_button(
                header='Salary Management',
                update_handlers=[self.state_manager.update_salary_df,
                                 self.state_manager.update_analysis_df
                ]
            )

            with st.form(key='salary_form'):
                if handle_salary_form(self.state_manager):
                    self.state_manager.update_salary_df()
                    self.state_manager.update_analysis_df()
                    # self.state_manager.update_all()

            st.header("Pension Growth Management")
            with st.form(key='pension_growth_form'):
                if handle_pension_growth_form(self.state_manager):
                    self.state_manager.update_salary_df()
                    self.state_manager.update_analysis_df()

        display_salary_sidebar(self.state_manager)
        display_pension_sidebar(self.state_manager)

        with st.expander("Combined Salary DataFrame", expanded=False):
            st.dataframe(self.state_manager.get_combined_salary_df())

        display_graph_plotly(
            title='Salary Graph',
            dataframe=self.state_manager.get_combined_salary_df(),
            default_columns=['Monthly Salary',
                             'Take Home Pay',
                             'Combined Pension Contribution'
            ]
        )

        display_graph_plotly(
            title='Pension Graph',
            dataframe=self.state_manager.get_combined_salary_df(),
            default_columns=['Running Total Pension',
                             ]
        )

class ExpensesUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            set_header_and_refresh_button(
                header='Expense Management',
                update_handlers=[self.state_manager.update_expense_df,
                                 self.state_manager.update_analysis_df
                                 ]
            )

            with st.form(key='expense_form'):
                if handle_expense_form(self.state_manager):
                    self.state_manager.update_expense_df()
                    self.state_manager.update_analysis_df()

        display_expense_sidebar(self.state_manager)

        with st.expander("Combined Expense DataFrame", expanded=False):
            # st.subheader("Combined Expense DataFrame")
            st.dataframe(self.state_manager.get_combined_expense_df())

        display_graph_plotly(
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
            set_header_and_refresh_button(
                header='Housing Management',
                update_handlers=[self.state_manager.update_house_df,
                                 self.state_manager.update_rent_df,
                                 self.state_manager.update_house_and_rent_df,
                                 self.state_manager.update_analysis_df
                                 ]
            )

            with st.form(key='housing_form'):
                if handle_house_form(self.state_manager):
                    self.state_manager.update_house_df()
                    self.state_manager.update_rent_df()
                    self.state_manager.update_house_and_rent_df()
                    self.state_manager.update_analysis_df()

            display_house_sidebar(self.state_manager)

            st.header("Rent Management")
            with st.form(key='rent_form'):
                if handle_rent_form(self.state_manager):
                    self.state_manager.update_house_df()
                    self.state_manager.update_rent_df()
                    self.state_manager.update_house_and_rent_df()
                    self.state_manager.update_analysis_df()

        display_rent_sidebar(self.state_manager)

        with st.expander("Combined Housing DataFrame", expanded=False):
            st.dataframe(self.state_manager.get_combined_house_df())

        with st.expander("Combined Rent DataFrame", expanded=False):
            st.dataframe(self.state_manager.get_combined_rent_df())

        with st.expander("Housing & Rent DataFrame", expanded=False):
            # st.subheader("Housing & Rent DataFrame")
            st.dataframe(self.state_manager.get_combined_house_and_rent_df())

        display_graph_plotly(
            title='Payments & Rent Graph',
            dataframe=self.state_manager.get_combined_house_and_rent_df(),
            default_columns=['Row Total Payment Amount',
                             'Row Total Interest Amount',
                             'Row Total Rent Amount'
                             ]
        )

        display_graph_plotly(
            title='Housing Equity Graph',
            dataframe=self.state_manager.get_combined_house_and_rent_df(),
            default_columns=['Row Total Remaining Balance Amount',
                             'Row Total Equity Amount',
                             ]
        )


class StockUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            set_header_and_refresh_button(
                header='Stock Management',
                update_handlers=[self.state_manager.update_stock_df,
                                 self.state_manager.update_analysis_df
                                 ]
            )

            with st.form(key='stock_form'):
                if handle_stock_form(self.state_manager):
                    self.state_manager.update_stock_df()
                    self.state_manager.update_analysis_df()

        display_stock_sidebar(self.state_manager)

        with st.expander("Combined Stock DataFrame", expanded=False):
            # st.subheader("Combined Stock DataFrame")
            st.dataframe(self.state_manager.get_combined_stock_df())

        display_graph_plotly(
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
            set_header_and_refresh_button(
                header='Asset Management',
                update_handlers=[self.state_manager.update_asset_df,
                                 self.state_manager.update_analysis_df
                                 ]
            )

            with st.form(key='asset_form'):
                if handle_asset_form(self.state_manager):
                    self.state_manager.update_asset_df()
                    self.state_manager.update_analysis_df()

        display_asset_sidebar(self.state_manager)

        with st.expander("Combined Asset DataFrame", expanded=False):
            # st.subheader("Combined Asset DataFrame")
            st.dataframe(self.state_manager.get_combined_asset_df())
        display_graph_plotly(
            title='Asset Graph',
            dataframe=self.state_manager.get_combined_asset_df(),
            default_columns=['Row Total Asset Value',
                             'Running Total Asset Value',
                             ]
        )

class AnalysisUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        set_header_and_refresh_button(
            header='Analysis',
            update_handlers=[self.state_manager.update_analysis_df
                             ]
        )

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

        display_graph_plotly(
            title='Analysis Graph - Monthly Brickdown',
            dataframe=self.state_manager.get_combined_analysis_df(),
            default_columns=['Monthly Cash Savings',
                             'Monthly Credit',
                             'Monthly Investment',
                             'Monthly Expenses',
                             'Monthly Losses'
                             ],
            y1=-5000,
            y2=10000
        )

        display_graph_plotly(
            title='Analysis Graph - Running Total',
            dataframe=self.state_manager.get_combined_analysis_df(),
            default_columns=['Running Total Cash Savings',
                             'Running Total Asset Amount',
                             'Running Total Cash & Asset',
                             'Running Total Cash & Asset & Pension'
                             ]
        )


class CompareSessionsUI:

    def __init__(self, state_manager):
        self.state_manager = state_manager

    def display(self):
        st.header("Compare Sessions")
        # Input for directory

        directorys = [f for f in os.listdir() if os.path.isdir(f)]
        directorys = clean_directory_list(directorys)
        default_index = get_index_of_value_in_list(directorys, 'saved_sessions')
        selected_directory = st.selectbox('Select a directory to load from:',
                                          directorys,
                                          key='select_directory_compare',
                                          index=default_index
        )

        # Get sessions in directory
        session_files = [f for f in os.listdir(selected_directory) if f.endswith(".json")]

        col1, col2 = st.columns([1, 1])
        # message_placeholder = st.empty()

        with col1:
            with st.container(border=True):
                st.subheader("Sessions 1")
                selected_file_1 = st.selectbox("Select a session to load:", session_files, key="select_session_1")

                if st.button("Load Session 1", key="loud_session_1"):
                    if selected_file_1:
                        session_json_1 = get_session_json_from_file(selected_directory, selected_file_1)
                        self.state_manager.set_session_1(session_json_1)
                        self.state_manager.update_compare_sessions()

            with st.expander("Sessions 1 DataFrame", expanded=False):  # key="expander_sessions_1"
                st.dataframe(self.state_manager.get_session_1_dataframe())

                # Add download button to download the combined analysis DataFrame as a CSV
                csv = self.state_manager.get_session_1_dataframe().to_csv(index=False)
                st.download_button(
                    label="Download DataFrame",
                    data=csv,
                    file_name='sessions_1.csv',
                    mime='text/csv',
                    key="download_sessions_1"
                )

            display_graph_overview(
                title='Sessions 1 Graph',
                dataframe=self.state_manager.get_session_1_dataframe(),
                default_columns=['Running Total Cash Savings',
                                 'Running Total Asset Amount',
                                 'Running Total Cash & Asset',
                                 'Running Total Cash & Asset & Pension',
                                 ],
                x1=0,
                x2=400,
                y1=0,
                y2=None,
                expanded=False
            )

        with col2:
            with st.container(border=True):
                st.subheader("Sessions 2")
                selected_file_2 = st.selectbox("Select a session to load:", session_files, key="select_session_2")

                if st.button("Load Session 2", key="loud_session_2"):
                    if selected_file_2:
                        session_2 = get_session_json_from_file(selected_directory, selected_file_2)
                        self.state_manager.set_session_2(session_2)
                        self.state_manager.update_compare_sessions()

            with st.expander("Sessions 2 DataFrame", expanded=False):  # key="expander_sessions_2"
                st.dataframe(self.state_manager.get_session_2_dataframe())

                # Add download button to download the combined analysis DataFrame as a CSV
                csv = self.state_manager.get_session_2_dataframe().to_csv(index=False)
                st.download_button(
                    label="Download DataFrame",
                    data=csv,
                    file_name='sessions_2.csv',
                    mime='text/csv',
                    key="download_sessions_2"
                )

            display_graph_overview(
                title='Sessions 2 Graph',
                dataframe=self.state_manager.get_session_2_dataframe(),
                default_columns=['Running Total Cash Savings',
                                 'Running Total Asset Amount',
                                 'Running Total Cash & Asset',
                                 'Running Total Cash & Asset & Pension',
                                 ],
                x1=0,
                x2=400,
                y1=0,
                y2=None,
                expanded=False
            )

        display_graph_plotly(
            title='Compare Sessions Monthly',
            dataframe=self.state_manager.get_compare_sessions_df(),
            default_columns=['S1 Monthly Cash Savings',
                             'S2 Monthly Cash Savings',
                             'Delta Monthly Cash Savings',
                             ],
            y1=-5000,
            y2=10000
        )

        display_graph_plotly(
            title='Compare Sessions Analysis',
            dataframe=self.state_manager.get_compare_sessions_df(),
            default_columns=['S1 Running Total Cash Savings',
                             'S2 Running Total Cash Savings',
                             'S1 Running Total Cash & Asset & Pension',
                             'S2 Running Total Cash & Asset & Pension',
                             ]
        )

        display_graph_plotly(
            title='Compare Sessions Delta (S1 - S2)',
            dataframe=self.state_manager.get_compare_sessions_df(),
            default_columns=['Delta Running Total Cash Savings',
                             'Delta Running Total Asset Amount',
                             'Delta Running Total Cash & Asset',
                             'Delta Running Total Cash & Asset & Pension',
                             ]
        )


