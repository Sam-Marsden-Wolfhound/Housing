import pandas as pd
import streamlit as st

def update_combined_salary_df():
    combined_df = pd.concat([salary['output_df'] for salary in st.session_state.salary_dfs], ignore_index=True)

    # Initialize the running total with compound interest
    running_total_pension = []
    current_total = 0

    for index, contribution in combined_df['Combined Pension Contribution'].items():
        current_total += contribution
        # Apply compound interest for the current month
        current_total *= (1 + st.session_state.pension_groth / 100 / 12)
        running_total_pension.append(current_total)

    combined_df['Running Total Pension'] = running_total_pension

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

    # Calculate the row sum of "Deposit" columns
    housing_deposit_columns = [col for col in combined_df.columns if 'Deposit for' in col]
    combined_df['Row Total Deposit Amount'] = combined_df[housing_deposit_columns].sum(axis=1)

    # Calculate the row sum of "Cashout Value" columns
    housing_cashout_columns = [col for col in combined_df.columns if 'Cashout Value for' in col]
    combined_df['Row Total Cashout Amount Housing'] = combined_df[housing_cashout_columns].sum(axis=1)

    st.session_state.combined_housing_df = combined_df


def update_combined_rent_df():
    # Concatenate all the output_df DataFrames along the columns
    combined_df = pd.concat([rent['output_df'] for rent in st.session_state.rent_dfs], axis=1)
    combined_df.fillna(0, inplace=True)

    # Calculate the row sum of "Rent Amount" columns
    rent_amount_columns = [col for col in combined_df.columns if 'Rent for' in col]
    combined_df['Row Total Rent Amount'] = combined_df[rent_amount_columns].sum(axis=1)

    # Store the combined DataFrame in session state
    st.session_state.combined_rent_df = combined_df

def update_combined_housing_and_rent_df():
    combined_df = pd.concat([st.session_state.combined_housing_df, st.session_state.combined_rent_df], axis=1)
    combined_df.fillna(0, inplace=True)
    st.session_state.combined_housing_and_rent_df = combined_df

def update_combined_stock_df():
    # Concatenate all the output_df DataFrames along the columns
    combined_df = pd.concat([stock['output_df'] for stock in st.session_state.stock_dfs], axis=1)
    combined_df.fillna(0, inplace=True)

    # Calculate the row sum of "Investment Amount" columns
    investment_amount_columns = [col for col in combined_df.columns if 'Investment Amount for' in col]
    combined_df['Row Total Investment Amount'] = combined_df[investment_amount_columns].sum(axis=1)

    # Calculate the row sum of "Cashout Value" columns
    cashout_value_columns = [col for col in combined_df.columns if 'Cashout Amount for' in col]
    combined_df['Row Total Cashout Amount Stocks'] = combined_df[cashout_value_columns].sum(axis=1)

    # Calculate the running sum for the "Row Total Investment Amount" column
    combined_df['Running Total Investment Amount'] = combined_df['Row Total Investment Amount'].cumsum()

    # Calculate the row sum of "Cash Value" columns
    cash_value_columns = [col for col in combined_df.columns if 'Cash Value for' in col]
    combined_df['Running Total Cash Value'] = combined_df[cash_value_columns].sum(axis=1)

    # Calculate the running sum for the "Row Total Cashout Value" column
    combined_df['Running Total Cashout Amount Stocks'] = combined_df['Row Total Cashout Amount Stocks'].cumsum()

    # Calculate the running sum for the Delta column
    combined_df['Delta'] = combined_df['Running Total Cashout Amount Stocks'] + combined_df['Running Total Cash Value'] - combined_df['Running Total Investment Amount']

    # Store the combined DataFrame in session state
    st.session_state.combined_stock_df = combined_df


def update_combined_savings_df():
    combined_df = pd.concat([asset['output_df'] for asset in st.session_state.savings_dfs], axis=1)

    # Calculate the row sum of "Asset Value" columns
    asset_value_columns = [col for col in combined_df.columns if 'Asset Value for' in col]
    combined_df['Row Total Asset Value'] = combined_df[asset_value_columns].sum(axis=1)
    combined_df.fillna(0, inplace=True)
    st.session_state.combined_savings_df = combined_df

def update_combined_analysis_df():

    combined_df = pd.concat([
        st.session_state.combined_salary_df,
        st.session_state.combined_expenses_df,
        st.session_state.combined_housing_and_rent_df,
        st.session_state.combined_stock_df,
        st.session_state.combined_savings_df
        ],
        axis=1,
        ignore_index=False
    )
    combined_df.fillna(0, inplace=True)

    combined_df['Monthly Credit'] = combined_df['Take Home Pay'] + combined_df['Row Total Cashout Amount Housing'] + combined_df['Row Total Rent Amount'] + combined_df['Row Total Cashout Amount Stocks'] + combined_df['Row Total Asset Value']
    combined_df['Monthly Investment'] = combined_df['Row Total Principal Payment Amount'] + combined_df['Row Total Investment Amount'] + combined_df['Row Total Deposit Amount']
    combined_df['Monthly Losses'] = combined_df['Monthly Expenses'] + combined_df['Row Total Interest Amount']
    combined_df['Monthly Cash Savings'] = combined_df['Monthly Credit'] - (combined_df['Monthly Investment'] + combined_df['Monthly Losses'])

    combined_df['Running Total Monthly Credit'] = combined_df['Monthly Credit'].cumsum()
    combined_df['Running Total Monthly Investment'] = combined_df['Monthly Investment'].cumsum()
    combined_df['Running Total Monthly Losses'] = combined_df['Monthly Losses'].cumsum()
    combined_df['Running Total Cash Savings'] = combined_df['Monthly Cash Savings'].cumsum()

    st.session_state.combined_analysis_df = combined_df