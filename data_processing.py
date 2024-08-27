import pandas as pd
import streamlit as st

def update_combined_salary_df():
    combined_df = pd.concat([salary['output_df'] for salary in st.session_state.salary_dfs], ignore_index=True)
    st.session_state.combined_salary_df = combined_df

def update_combined_expenses_df():
    combined_df = pd.concat([expense['output_df'] for expense in st.session_state.expenses_dfs], ignore_index=True)
    st.session_state.combined_expenses_df = combined_df

def update_combined_housing_df():
    combined_df = pd.concat([house['output_df'] for house in st.session_state.housing_dfs], axis=1)
    combined_df.fillna(0, inplace=True)
    # print(combined_df)
    st.session_state.combined_housing_df = combined_df