import streamlit as st
import pandas as pd

def initialize_state():
    # Input DFs
    if 'salary_dfs' not in st.session_state:
        st.session_state['salary_dfs'] = []
    if 'expenses_dfs' not in st.session_state:
        st.session_state['expenses_dfs'] = []
    if 'housing_dfs' not in st.session_state:
        st.session_state['housing_dfs'] = []
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
    if 'editing_stock_index' not in st.session_state:
        st.session_state['editing_stock_index'] = None
    if 'editing_savings_index' not in st.session_state:
        st.session_state['editing_savings_index'] = None
    # if 'housing_df_timeframe' not in st.session_state:
    #     st.session_state['housing_df_timeframe'] = 40

    if 'combined_salary_df' not in st.session_state:
        st.session_state['combined_salary_df'] = pd.DataFrame()
    if 'combined_expenses_df' not in st.session_state:
        st.session_state['combined_expenses_df'] = pd.DataFrame()
    if 'combined_housing_df' not in st.session_state:
        st.session_state['combined_housing_df'] = pd.DataFrame()
    if 'combined_stock_df' not in st.session_state:
        st.session_state['combined_stock_df'] = pd.DataFrame()
    if 'combined_savings_df' not in st.session_state:
        st.session_state['combined_savings_df'] = pd.DataFrame()

def clear_state():
    st.session_state.clear()
