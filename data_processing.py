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


def update_combined_stock_df():
    # Concatenate all the output_df DataFrames along the columns
    combined_df = pd.concat([stock['output_df'] for stock in st.session_state.stock_dfs], axis=1)
    combined_df.fillna(0, inplace=True)

    # Calculate the row sum of "Investment Amount" columns
    investment_amount_columns = [col for col in combined_df.columns if 'Investment Amount for' in col]
    combined_df['Row Total Investment Amount'] = combined_df[investment_amount_columns].sum(axis=1)

    # Calculate the row sum of "Cashout Value" columns
    cashout_value_columns = [col for col in combined_df.columns if 'Cashout Value for' in col]
    combined_df['Row Total Cashout Value'] = combined_df[cashout_value_columns].sum(axis=1)

    # Calculate the running sum for the "Row Total Investment Amount" column
    combined_df['Running Total Investment Amount'] = combined_df['Row Total Investment Amount'].cumsum()

    # Calculate the row sum of "Cash Value" columns
    cash_value_columns = [col for col in combined_df.columns if 'Cash Value for' in col]
    combined_df['Running Total Cash Value'] = combined_df[cash_value_columns].sum(axis=1)

    # Calculate the running sum for the "Row Total Cashout Value" column
    combined_df['Running Total Cashout Value'] = combined_df['Row Total Cashout Value'].cumsum()

    # Calculate the running sum for the Delta column
    combined_df['Delta'] = combined_df['Running Total Cashout Value'] + combined_df['Running Total Cash Value'] - combined_df['Running Total Investment Amount']

    # Store the combined DataFrame in session state
    st.session_state.combined_stock_df = combined_df


def update_combined_savings_df():
    combined_df = pd.concat([asset['output_df'] for asset in st.session_state.savings_dfs], axis=1)

    # Calculate the row sum of "Asset Value" columns
    asset_value_columns = [col for col in combined_df.columns if 'Asset Value for' in col]
    combined_df['Row Total Asset Value'] = combined_df[asset_value_columns].sum(axis=1)
    combined_df.fillna(0, inplace=True)
    st.session_state.combined_savings_df = combined_df