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

    # Calculate the row sum of "Payment" columns
    housing_cashout_columns = [col for col in combined_df.columns if 'Payment for' in col]
    combined_df['Row Total Payment Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

    # Calculate the row sum of "Interest" columns
    housing_cashout_columns = [col for col in combined_df.columns if 'Interest Payment for' in col]
    combined_df['Row Total Interest Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

    # Calculate the row sum of "Principal Payment" columns
    housing_cashout_columns = [col for col in combined_df.columns if 'Principal Payment for' in col]
    combined_df['Row Total Principal Payment Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

    # Calculate the row sum of "Remaining Balance" columns
    housing_cashout_columns = [col for col in combined_df.columns if 'Remaining Balance for' in col]
    combined_df['Row Total Remaining Balance Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

    # Calculate the row sum of "Equity" columns
    housing_cashout_columns = [col for col in combined_df.columns if 'Equity for' in col]
    combined_df['Row Total Equity Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

    # Calculate the row sum of "Cashout Value" columns
    housing_cashout_columns = [col for col in combined_df.columns if 'Cashout Value for' in col]
    combined_df['Row Total Cashout Amount'] = combined_df[housing_cashout_columns].sum(axis=1)

    st.session_state.combined_housing_df = combined_df


def update_combined_rent_df():
    pass

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