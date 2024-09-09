import os
import time
import pickle
import pandas as pd
import streamlit as st
from data_processing import update_combined_salary_df, update_combined_expenses_df, update_combined_housing_df, update_combined_rent_df, update_combined_housing_and_rent_df, update_combined_stock_df, update_combined_savings_df, update_combined_analysis_df



class StateManager:
    def __init__(self):
        print("Initialize state manager")

        if "session" not in st.session_state:
            st.session_state.session = Session()
        if "ui_state" not in st.session_state:
            st.session_state.ui_state = UiState()
            pass
        self.session = st.session_state.session
        self.ui_state = st.session_state.ui_state


    # Session -----------------------------------------------------------------
    def get_current_session(self):
        return self.session

    def load_session_as_current_session(self, loaded_state):
        self.session = None
        self.session = loaded_state

    def add_salary_df(self, obj):
        self.session.add_salary_df(obj)

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

    def get_combined_salary_df(self):
        return self.session.get_combined_salary_df()


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
        print("Initialize Session")
        # Input DFs
        self.salary_dfs = []
        self.pension_dfs = []
        self.expense_dfs = []
        self.house_dfs = []
        self.rent_dfs = []
        self.stock_dfs = []
        self.asset_dfs = []

        # Combined DF's
        self.combined_salary_df = pd.DataFrame()
        self.combined_expenses_df = pd.DataFrame()
        self.combined_housing_df = pd.DataFrame()
        self.combined_rent_df = pd.DataFrame()
        self.combined_housing_and_rent_df = pd.DataFrame()
        self.combined_stock_df = pd.DataFrame()
        self.combined_savings_df = pd.DataFrame()
        self.combined_analysis_df = pd.DataFrame()


    def add_salary_df(self, obj):
        self.salary_dfs.append(obj)

    def add_pension_df(self, obj):
        self.pension_dfs.append(obj)

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

    def get_pension_dfs(self):
        return self.pension_dfs

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

    def initialise_combined_salary_df(self):
        pass



#-------------------------------------------------------------------------------------------
class UiState:

    def __init__(self):
        print("Initialize UiState")
        self.form_id_key = [
            'next_salary_id',
            'next_expense_id',
            'next_housing_id',
            'next_rent_id',
            'next_stock_id',
            'next_asset_id'
        ]
        self.form_id = {}
        self.initialise_form_ids()
        self.editing_index_key = [
            'editing_salary_index',
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
        # self.ui_update_handlers['combined_salary_df_update_handler'] = update_combined_expenses_df
        # self.ui_update_handlers['combined_salary_df_update_handler'] = update_combined_housing_df
        # self.ui_update_handlers['combined_salary_df_update_handler'] = update_combined_rent_df
        # self.ui_update_handlers['combined_salary_df_update_handler'] = update_combined_housing_and_rent_df
        # self.ui_update_handlers['combined_salary_df_update_handler'] = update_combined_stock_df
        # self.ui_update_handlers['combined_salary_df_update_handler'] = update_combined_savings_df
        # self.ui_update_handlers['combined_salary_df_update_handler'] = update_combined_analysis_df

    def update_all(self, session):
        print('updating all')
        for handler_key in self.ui_update_handlers:
            # print(handler_key, self.ui_update_handlers[handler_key])
            self.ui_update_handlers[handler_key](session)


#-------------------------------------------------------------------------------------------
def save_session_state(state_manager, directory, file_name, use_uuid):
    """Save the current session state to a file."""
    if not os.path.exists(directory):
        os.makedirs(directory)

    name_prefix = "Session_"
    if use_uuid:
        filename = f"{name_prefix}{file_name}_{int(time.time())}.pkl"
    else:
        filename = f"{name_prefix}{file_name}.pkl"

    filepath = os.path.join(directory, filename)

    with open(filepath, "wb") as f:
        pickle.dump(state_manager.get_current_session(), f)

    st.success(f"Session saved as {filename}")
    # Need a message System


def update_session_state(state_manager, directory, file_name):
    filepath = os.path.join(directory, file_name)

    with open(filepath, "wb") as f:
        pickle.dump(state_manager.get_current_session(), f)

    st.success(f"Session updated {file_name}")


def clear_state():
    st.session_state.clear()


def load_session_state(state_manager, file_path):
    """Load a session state from a file."""
    with open(file_path, "rb") as f:
        loaded_state = pickle.load(f)

    state_manager.load_session_as_current_session(loaded_state)

    st.success(f"Session loaded from {os.path.basename(file_path)}!")


def load_session_state_old(file_path):
    """Load a session state from a file."""
    with open(file_path, "rb") as f:
        loaded_state = pickle.load(f)
        # time.sleep(0.1)

    # Print out the contents to see what is stored
    # print(loaded_state)

    if loaded_state:
        # Merge loaded state into session state
        # for key, value in loaded_state.items():
        #     print(key)
        key_list = [
            'salary_dfs',
            'expenses_dfs',
            'housing_dfs',
            'rent_dfs',
            'stock_dfs',
            'savings_dfs']

        for key in key_list:
            st.session_state[key] = loaded_state[key]
    else:
        st.warning("Loaded state is empty. No changes were made.")

    # Clear the current session state and update it with the loaded state
    # st.session_state.clear()
    # time.sleep(0.3)
    # st.session_state.update(loaded_state)

    st.success(f"Session loaded from {os.path.basename(file_path)}!")








def initialize_state():
    # Input DFs
    if 'salary_dfs' not in st.session_state:
        st.session_state['salary_dfs'] = []
    if 'expenses_dfs' not in st.session_state:
        st.session_state['expenses_dfs'] = []
    if 'housing_dfs' not in st.session_state:
        st.session_state['housing_dfs'] = []
    if 'rent_dfs' not in st.session_state:
        st.session_state['rent_dfs'] = []
    if 'stock_dfs' not in st.session_state:
        st.session_state['stock_dfs'] = []
    if 'savings_dfs' not in st.session_state:
        st.session_state['savings_dfs'] = []

    # Form ID
    if 'next_salary_id' not in st.session_state:
        st.session_state['next_salary_id'] = 1
    if 'next_expense_id' not in st.session_state:
        st.session_state['next_expense_id'] = 1
    if 'next_housing_id' not in st.session_state:
        st.session_state['next_housing_id'] = 1
    if 'next_rent_id' not in st.session_state:
        st.session_state['next_rent_id'] = 1
    if 'next_stock_id' not in st.session_state:
        st.session_state['next_stock_id'] = 1
    if 'next_savings_id' not in st.session_state:
        st.session_state['next_savings_id'] = 1

    # Index
    if 'editing_salary_index' not in st.session_state:
        st.session_state['editing_salary_index'] = None
    if 'editing_expense_index' not in st.session_state:
        st.session_state['editing_expense_index'] = None
    if 'editing_house_index' not in st.session_state:
        st.session_state['editing_house_index'] = None
    if 'editing_rent_index' not in st.session_state:
        st.session_state['editing_rent_index'] = None
    if 'editing_stock_index' not in st.session_state:
        st.session_state['editing_stock_index'] = None
    if 'editing_savings_index' not in st.session_state:
        st.session_state['editing_savings_index'] = None
    # if 'housing_df_timeframe' not in st.session_state:
    #     st.session_state['housing_df_timeframe'] = 40

    # Combined DF's
    if 'combined_salary_df' not in st.session_state:
        st.session_state['combined_salary_df'] = pd.DataFrame()
    if 'combined_expenses_df' not in st.session_state:
        st.session_state['combined_expenses_df'] = pd.DataFrame()
    if 'combined_housing_df' not in st.session_state:
        st.session_state['combined_housing_df'] = pd.DataFrame()
    if 'combined_rent_df' not in st.session_state:
        st.session_state['combined_rent_df'] = pd.DataFrame()
    if 'combined_housing_and_rent_df' not in st.session_state:
        st.session_state['combined_housing_and_rent_df'] = pd.DataFrame()
    if 'combined_stock_df' not in st.session_state:
        st.session_state['combined_stock_df'] = pd.DataFrame()
    if 'combined_savings_df' not in st.session_state:
        st.session_state['combined_savings_df'] = pd.DataFrame()
    if 'combined_analysis_df' not in st.session_state:
        st.session_state['combined_analysis_df'] = pd.DataFrame()

    # Global Values
    if 'pension_groth' not in st.session_state:
        st.session_state['pension_groth'] = 3.5

def clear_state():
    st.session_state.clear()


