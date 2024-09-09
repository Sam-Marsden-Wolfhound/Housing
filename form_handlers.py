import pandas as pd
import streamlit as st
from data_processing import create_salary_output_df, create_expense_output_df, create_housing_output_df, create_rent_output_df,create_stock_output_df, create_savings_output_df


def handle_salary_form(state_manager):
    default_name = f"Salary {state_manager.get_form_id(key='next_salary_id')}"
    name = st.text_input("Salary Name", value=default_name)
    annual_income = st.number_input("Annual Gross Income", value=60000)
    pension_contrib = st.number_input("Pension Contribution (%)", value=3.0)
    company_match = st.number_input("Company Match (%)", value=3.0)
    num_months = st.number_input("Number of Months", value=12, min_value=1)

    if st.form_submit_button("Add Salary"):
        output_df = create_salary_output_df(annual_income, pension_contrib, company_match, num_months)
        state_manager.add_salary_df({
            'name': name,
            'output_df': output_df,
            'annual_income': annual_income,
            'pension_contrib': pension_contrib,
            'company_match': company_match,
            'num_months': num_months
        })
        state_manager.add_one_to_form_id(key='next_salary_id')
        return True
    return False


def handle_expense_form():
    default_name = f"Expense {st.session_state.next_expense_id}"
    name = st.text_input("Expense Name", value=default_name)
    monthly_expense = st.number_input("Monthly Expenses", value=1000.00)
    months = st.number_input("Months", value=12, min_value=1)

    if st.form_submit_button("Add Expense"):
        output_df = create_expense_output_df(monthly_expense, months)
        st.session_state.expenses_dfs.append({
            'name': name,
            'output_df': output_df,
            'monthly_expense': monthly_expense,
            'months': months
        })
        st.session_state.next_expense_id += 1
        return True
    return False

def handle_housing_form():
    """Handles the housing input form and returns the data."""
    st.write("Add a new house")
    default_name = f"House {st.session_state.get('next_housing_id', 1)}"
    name = st.text_input("House Name", value=default_name)
    house_value = st.number_input("House Value", value=200000)
    acquisition_month = st.number_input("Month of Acquisition", value=0)
    appreciation_rate = st.number_input("House Appreciation Rate (%)", value=1.5)

    # Mortgage related inputs
    with st.expander("Mortgage Details", expanded=False):
        mortgage = st.checkbox("Mortgage")
        deposit = st.number_input("Deposit", value=50000)
        mortgage_term = st.number_input("Mortgage Term (years)", value=25)
        interest_rate = st.number_input("Interest Rate (%)", value=3.5)
    if not mortgage:
        deposit = None
        mortgage_term = None
        interest_rate = None

    # Sale related inputs
    with st.expander("Sale Details", expanded=False):
        sale = st.checkbox("Sell House")
        sale_month = st.number_input("Month of Sale", value=acquisition_month + 300, min_value=acquisition_month + 1)
    if not sale:
        sale_month = None

    if st.form_submit_button("Add House"):
        output_df = create_housing_output_df(
            name,
            house_value,
            acquisition_month,
            appreciation_rate,
            mortgage,
            deposit,
            mortgage_term,
            interest_rate,
            sale,
            sale_month
        )
        if 'housing_dfs' not in st.session_state:
            st.session_state.housing_dfs = []

        st.session_state.housing_dfs.append({
            'name': name,
            'house_value': house_value,
            'acquisition_month': acquisition_month,
            'appreciation_rate': appreciation_rate,
            'mortgage': mortgage,
            'deposit': deposit,
            'mortgage_term': mortgage_term,
            'interest_rate': interest_rate,
            'sale': sale,
            'sale_month': sale_month,
            'output_df': output_df,
        })

        st.session_state.next_housing_id += 1
        return True
    return False

def handle_rent_form():
    default_name = f"Rent {st.session_state.next_rent_id}"
    name = st.text_input("Rent Name", value=default_name)
    rent_amount = st.number_input("Rent Amount", value=2000)
    start_month = st.number_input("Starting Month", value=0)
    duration = st.number_input("Duration", value=12, min_value=0)

    if st.form_submit_button("Add Rent"):
        output_df = create_rent_output_df(name, rent_amount, start_month, duration)

        st.session_state.rent_dfs.append({
            'name': name,
            'rent_amount': rent_amount,
            'start_month': start_month,
            'duration': duration,
            'output_df': output_df,
        })
        st.session_state.next_rent_id += 1
        return True
    return False

def handle_stock_form():
    default_name = f"Stock {st.session_state.next_stock_id}"
    name = st.text_input("Stock Name", value=default_name)
    acquisition_month = st.number_input("Acquisition Month", value=0)
    investment_amount = st.number_input("Dollar-Cost Averaging Amount (£)", value=100, min_value=0)
    months_buying_stock = st.number_input("Dollar-Cost Averaging Months", value=60, min_value=0)
    appreciation_rate = st.number_input("Appreciation Rate (%)", value=3)
    with st.expander("Sale Details", expanded=False):
        sale = st.checkbox("Sell Stock")
        sale_month = st.number_input("Month of Sale", value=acquisition_month + months_buying_stock + 1, min_value=acquisition_month + months_buying_stock + 1)
    if not sale:
        sale_month = None

    if st.form_submit_button("Add Stock"):
        output_df = create_stock_output_df(name, appreciation_rate, investment_amount, acquisition_month, months_buying_stock, sale, sale_month)

        st.session_state.stock_dfs.append({
            'name': name,
            'acquisition_month': acquisition_month,
            'investment_amount': investment_amount,
            'months_buying_stock': months_buying_stock,
            'appreciation_rate': appreciation_rate,
            'sale': sale,
            'sale_month': sale_month,
            'output_df': output_df,
        })

        st.session_state.next_stock_id += 1
        return True
    return False

def handle_savings_form():
    default_name = f"Asset {st.session_state.next_savings_id}"
    name = st.text_input("Asset Name", value=default_name)
    asset_value = st.number_input("Asset Value", value=1000.00)
    acquisition_month = st.number_input("Acquisition Month", value=0, min_value=0)

    if st.form_submit_button("Add Asset"):
        output_df = create_savings_output_df(name, asset_value, acquisition_month)
        st.session_state.savings_dfs.append({
            'name': name,
            'asset_value': asset_value,
            'acquisition_month': acquisition_month,
            'output_df': output_df,
        })
        st.session_state.next_savings_id += 1
        return True
    return False


