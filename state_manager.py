import streamlit as st
import pandas as pd

def initialize_state():
    if 'salary_dfs' not in st.session_state:
        st.session_state['salary_dfs'] = []
    if 'expenses_dfs' not in st.session_state:
        st.session_state['expenses_dfs'] = []
    if 'next_salary_id' not in st.session_state:
        st.session_state['next_salary_id'] = 1
    if 'next_expense_id' not in st.session_state:
        st.session_state['next_expense_id'] = 1
    if 'editing_salary_index' not in st.session_state:
        st.session_state['editing_salary_index'] = None
    if 'editing_expense_index' not in st.session_state:
        st.session_state['editing_expense_index'] = None
    if 'combined_salary_df' not in st.session_state:
        st.session_state['combined_salary_df'] = pd.DataFrame()
    if 'combined_expenses_df' not in st.session_state:
        st.session_state['combined_expenses_df'] = pd.DataFrame()

def clear_state():
    st.session_state.clear()
