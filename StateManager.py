import os
import time
import pickle
import pandas as pd
import streamlit as st
from data_processing import update_combined_salary_df, update_combined_expense_df, update_combined_house_df, update_combined_rent_df, update_combined_house_and_rent_df, update_combined_stock_df, update_combined_asset_df, update_combined_analysis_df

class StateManager:
    def __init__(self):
        # print("Initialize state manager")

        if "session" not in st.session_state:
            st.session_state.session = Session()
        if "ui_state" not in st.session_state:
            st.session_state.ui_state = UiState()
        if "comp_session_1" not in st.session_state:
            st.session_state.comp_session_1 = Session()
        if "comp_session_2" not in st.session_state:
            st.session_state.comp_session_2 = Session()
        # Set Refs
        self.session = st.session_state.session
        self.ui_state = st.session_state.ui_state
        self.comp_session_1 = st.session_state.comp_session_1
        self.comp_session_2 = st.session_state.comp_session_2


    # Session -----------------------------------------------------------------
    def get_current_session(self):
        return self.session
        # return st.session_state.session

    def load_session_as_current_session(self, loaded_state):
        st.session_state.session = None
        st.session_state.session = loaded_state
        st.session_state.ui_state = None
        st.session_state.ui_state = UiState()
        # self.session = None
        # self.session = loaded_state

    def new_session_state(self):
        st.session_state.session = Session()

    def set_user_age(self, age):
        self.session.set_user_age(age)

    def get_user_age(self):
        return self.session.get_user_age()

    def add_salary_df(self, obj):
        self.session.add_salary_df(obj)

    def add_pension_growth_df(self, obj):
        self.session.add_pension_growth_df(obj)

    def add_expense_df(self, obj):
        self.session.add_expense_df(obj)

    def add_house_df(self, obj):
        self.session.add_house_df(obj)

    def add_rent_df(self, obj):
        self.session.add_rent_df(obj)

    def add_stock_df(self, obj):
        self.session.add_stock_df(obj)

    def add_asset_df(self, obj):
        self.session.add_asset_df(obj)

    def get_salary_dfs(self):
        return self.session.get_salary_dfs()

    def get_pension_growth_dfs(self):
        return self.session.get_pension_growth_dfs()

    def get_expense_dfs(self):
        return self.session.get_expense_dfs()

    def get_house_dfs(self):
        return self.session.get_house_dfs()

    def get_rent_dfs(self):
        return self.session.get_rent_dfs()

    def get_stock_dfs(self):
        return self.session.get_stock_dfs()

    def get_asset_dfs(self):
        return self.session.get_asset_dfs()

    def get_combined_salary_df(self):
        return self.session.get_combined_salary_df()

    def get_combined_expense_df(self):
        return self.session.get_combined_expense_df()

    def get_combined_house_df(self):
        return self.session.get_combined_house_df()

    def get_combined_rent_df(self):
        return self.session.get_combined_rent_df()

    def get_combined_house_and_rent_df(self):
        return self.session.get_combined_house_and_rent_df()

    def get_combined_stock_df(self):
        return self.session.get_combined_stock_df()

    def get_combined_asset_df(self):
        return self.session.get_combined_asset_df()

    def get_combined_analysis_df(self):
        return self.session.get_combined_analysis_df()

    # Compare Sessions
    def set_session_1(self, session):
        st.session_state.comp_session_1 = session
        self.comp_session_1 = st.session_state.comp_session_1

    def set_session_2(self, session):
        st.session_state.comp_session_2 = session
        self.comp_session_2 = st.session_state.comp_session_2

    def get_session_1_dataframe(self):
        return self.comp_session_1.get_combined_analysis_df()

    def get_session_2_dataframe(self):
        return self.comp_session_2.get_combined_analysis_df()



    # UI State ----------------------------------------------------------------
    def get_current_ui_state(self):
        return self.ui_state

    def get_form_id(self, key):
        return self.ui_state.get_form_id(key)

    def add_one_to_form_id(self, key):
        self.ui_state.add_one_to_form_id(key)

    def get_editing_index(self, key):
        return self.ui_state.get_editing_index(key)

    def set_editing_index(self, key, value):
        self.ui_state.set_editing_index(key, value)

    def update_all(self):
        self.ui_state.update_all(self.session)


#------------------------------------------------------------------------------------
class Session:

    def __init__(self):
        # print("Initialize Session")
        self.version = 1

        # User Inputes
        self.user_age = 0

        # Input DFs
        self.salary_dfs = []
        self.pension_growth_dfs = []
        self.expense_dfs = []
        self.house_dfs = []
        self.rent_dfs = []
        self.stock_dfs = []
        self.asset_dfs = []

        # Combined DF's
        self.combined_salary_df = pd.DataFrame()
        self.combined_expense_df = pd.DataFrame()
        self.combined_house_df = pd.DataFrame()
        self.combined_rent_df = pd.DataFrame()
        self.combined_house_and_rent_df = pd.DataFrame()
        self.combined_stock_df = pd.DataFrame()
        self.combined_asset_df = pd.DataFrame()
        self.combined_analysis_df = pd.DataFrame()

    def get_version(self):
        return self.version

    def set_user_age(self, age):
        self.user_age = age

    def get_user_age(self):
        return self.user_age

    def add_salary_df(self, obj):
        self.salary_dfs.append(obj)

    def add_pension_growth_df(self, obj):
        self.pension_growth_dfs.append(obj)

    def add_expense_df(self, obj):
        self.expense_dfs.append(obj)

    def add_house_df(self, obj):
        self.house_dfs.append(obj)

    def add_rent_df(self, obj):
        self.rent_dfs.append(obj)

    def add_stock_df(self, obj):
        self.stock_dfs.append(obj)

    def add_asset_df(self, obj):
        self.asset_dfs.append(obj)

    def get_salary_dfs(self):
        return self.salary_dfs

    def get_pension_growth_dfs(self):
        return self.pension_growth_dfs

    def get_expense_dfs(self):
        return self.expense_dfs

    def get_house_dfs(self):
        return self.house_dfs

    def get_rent_dfs(self):
        return self.rent_dfs

    def get_stock_dfs(self):
        return self.stock_dfs

    def get_asset_dfs(self):
        return self.asset_dfs

    def get_combined_salary_df(self):
        return self.combined_salary_df

    def get_combined_expense_df(self):
        return self.combined_expense_df

    def get_combined_house_df(self):
        return self.combined_house_df

    def get_combined_rent_df(self):
        return self.combined_rent_df

    def get_combined_house_and_rent_df(self):
        return self.combined_house_and_rent_df

    def get_combined_stock_df(self):
        return self.combined_stock_df

    def get_combined_asset_df(self):
        return self.combined_asset_df

    def get_combined_analysis_df(self):
        return self.combined_analysis_df


#-------------------------------------------------------------------------------------------
class UiState:

    def __init__(self):
        # print("Initialize UiState")
        self.form_id_key = [
            'next_salary_id',
            'next_pension_id',
            'next_expense_id',
            'next_house_id',
            'next_rent_id',
            'next_stock_id',
            'next_asset_id'
        ]
        self.form_id = {}
        self.initialise_form_ids()
        self.editing_index_key = [
            'editing_salary_index',
            'editing_pension_index',
            'editing_expense_index',
            'editing_house_index',
            'editing_rent_index',
            'editing_stock_index',
            'editing_asset_index'
        ]
        self.editing_index = {}
        self.initialise_editing_index()

        self.ui_update_handlers = {}
        self.add_update_handlers()


    def initialise_form_ids(self):
        for id in self.form_id_key:
            if id not in self.form_id:
                self.form_id[id] = 1

    def get_form_id(self, key):
        return self.form_id[key]

    def add_one_to_form_id(self, key):
        self.form_id[key] += 1

    def initialise_editing_index(self):
        for index in self.editing_index_key:
            if index not in self.editing_index:
                self.editing_index[index] = None

    def get_editing_index(self, key):
        return self.editing_index[key]

    def set_editing_index(self, key, value):
        self.editing_index[key] = value

    def add_combined_salary_df_update_handler(self, update_handler):
        self.ui_update_handlers['combined_salary_df_update_handler'] = update_handler

    def add_update_handlers(self):
        self.ui_update_handlers['combined_salary_df_update_handler'] = update_combined_salary_df
        self.ui_update_handlers['combined_expense_df_update_handler'] = update_combined_expense_df
        self.ui_update_handlers['combined_house_df_update_handler'] = update_combined_house_df
        self.ui_update_handlers['combined_rent_df_update_handler'] = update_combined_rent_df
        self.ui_update_handlers['combined_house_and_rent_df_update_handler'] = update_combined_house_and_rent_df
        self.ui_update_handlers['combined_stock_df_update_handler'] = update_combined_stock_df
        self.ui_update_handlers['combined_asset_df_update_handler'] = update_combined_asset_df
        self.ui_update_handlers['combined_analysis_df_update_handler'] = update_combined_analysis_df

    def update_all(self, session):
        # print('updating all')
        for handler_key in self.ui_update_handlers:
            # print(handler_key, self.ui_update_handlers[handler_key])
            self.ui_update_handlers[handler_key](session)

        # st.write(
        #     """
        #     <script>
        #     location.reload();
        #     </script>
        #     """,
        #     unsafe_allow_html=True
        # )


#-------------------------------------------------------------------------------------------
def save_session_state(state_manager, directory, file_name, use_uuid, message):
    """Save the current session state to a file."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    # name_prefix = "Session_"
    name_prefix = ""
    if use_uuid:
        filename = f"{name_prefix}{file_name}_{int(time.time())}.pkl"
    else:
        filename = f"{name_prefix}{file_name}.pkl"

    filepath = os.path.join(directory, filename)

    with open(filepath, "wb") as f:
        pickle.dump(state_manager.get_current_session(), f)

    message.success(f"Session saved as {filename}")
    # Need a message System


def update_session_state(state_manager, directory, selected_file, messager):
    if not directory == None and not selected_file == None:
        filepath = os.path.join(directory, selected_file)

        # Check if the file exists and delete it before writing the new one
        if os.path.exists(filepath):
            os.remove(filepath)

        with open(filepath, "wb") as f:
            pickle.dump(state_manager.get_current_session(), f)

        messager.success(f"Session updated {selected_file}")


def load_session_state(state_manager, directory, selected_file, messager):
    if not directory == None and not selected_file == None:
        file_path = os.path.join(directory, selected_file)

        """Load a session state from a file."""
        with open(file_path, "rb") as f:
            loaded_state = pickle.load(f)

        state_manager.load_session_as_current_session(loaded_state)

        messager.success(f"Session loaded from {os.path.basename(file_path)} \nVersion: {loaded_state.get_version()}")

def get_session_from_file(directory, selected_file):
    if not directory == None and not selected_file == None:
        file_path = os.path.join(directory, selected_file)

        """Load a session state from a file."""
        with open(file_path, "rb") as f:
            loaded_state = pickle.load(f)

        return loaded_state
    return None


def new_session_state(state_manager):
    state_manager.new_session_state()


def delete_session(directory, selected_file, messager):
    if not directory == None and not selected_file == None:
        filepath = os.path.join(directory, selected_file)

        # Check if the file exists and delete it before writing the new one
        if os.path.exists(filepath):
            os.remove(filepath)
            messager.success(f"Deleted Session {selected_file}")
        pass

    else:
        messager.error(f"No file to delete")


def clear_state():
    st.session_state.clear()