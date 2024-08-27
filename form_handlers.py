import pandas as pd
import streamlit as st


def handle_salary_form():
    default_name = f"Salary {st.session_state.next_salary_id}"
    name = st.text_input("Salary Name", value=default_name)
    annual_income = st.number_input("Annual Gross Income", value=60000)
    pension_contrib = st.number_input("Pension Contribution (%)", value=3.0)
    company_match = st.number_input("Company Match (%)", value=3.0)
    num_months = st.number_input("Number of Months", value=12, min_value=1, max_value=120)

    if st.form_submit_button("Add Salary"):
        output_df = create_salary_output_df(annual_income, pension_contrib, company_match, num_months)
        st.session_state.salary_dfs.append({
            'name': name,
            'output_df': output_df,
            'annual_income': annual_income,
            'pension_contrib': pension_contrib,
            'company_match': company_match,
            'num_months': num_months
        })
        st.session_state.next_salary_id += 1
        return True
    return False


def handle_expense_form():
    default_name = f"Expense {st.session_state.next_expense_id}"
    name = st.text_input("Expense Name", value=default_name)
    monthly_expense = st.number_input("Monthly Expenses", value=1000.00)
    months = st.number_input("Months", value=12, min_value=1, max_value=120)

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
        sale_month = st.number_input("Month of Sale", value=acquisition_month + 1, min_value=acquisition_month + 1)
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


def create_salary_output_df(annual_income, pension_contrib, company_match, num_months):
    monthly_salary = annual_income / num_months
    pension_deduction = (pension_contrib / 100) * monthly_salary
    combined_pension_contribution = pension_deduction + (company_match / 100) * monthly_salary
    take_home_pay = monthly_salary - pension_deduction

    output_data = {
        'Monthly Salary': [monthly_salary] * num_months,
        'Pension Deduction': [pension_deduction] * num_months,
        'Combined Pension Contribution': [combined_pension_contribution] * num_months,
        'Take Home Pay': [take_home_pay] * num_months
    }
    return pd.DataFrame(output_data)


def create_expense_output_df(monthly_expense, months):
    return pd.DataFrame({'Monthly Expenses': [monthly_expense] * months})

def create_housing_output_df(name, og_house_value, acquisition_month, appreciation_rate, mortgage, deposit, mortgage_term, interest_rate, sale, sale_month):
    if sale:
        ownership_months = sale_month - acquisition_month
    else:
        ownership_months = 1200  # 100 years

    house_value = og_house_value
    monthly_appreciation_rate = (appreciation_rate / 100) / 12

    house_values = []
    payments = []
    interest_payments = []
    principal_payments = []
    remaining_balances = []
    equitys = []

    if mortgage:
        borrowed_capital = og_house_value - deposit
        remaining_balance = borrowed_capital
        monthly_interest_rate = (interest_rate/100) / 12
        number_of_payments = mortgage_term * 12
        monthly_payment = ((borrowed_capital * monthly_interest_rate) /
                           (1 - (1 + monthly_interest_rate) ** -number_of_payments))
    else:
        number_of_payments = 0

    for month in range(acquisition_month):
        house_values.append(0)
        payments.append(0)
        interest_payments.append(0)
        principal_payments.append(0)
        remaining_balances.append(0)
        equitys.append(0)

    for month in range(ownership_months):
        if not mortgage:
            monthly_payment = 0
            interest_payment = 0
            principal_payment = 0
            remaining_balance = 0

        elif month >= number_of_payments:
            monthly_payment = 0
            interest_payment = 0
            principal_payment = 0
            remaining_balance = 0

        else:
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

        house_values.append(house_value)
        payments.append(monthly_payment)
        interest_payments.append(interest_payment)
        principal_payments.append(principal_payment)
        remaining_balances.append(remaining_balance)
        equitys.append(house_value-remaining_balance)

        house_value += house_value * monthly_appreciation_rate

    output_data = {
        f'House Value for {name}': house_values,
        f'Payment for {name}': payments,
        f'Interest Payment for {name}': interest_payments,
        f'Principal Payment for {name}': principal_payments,
        f'Remaining Balance for {name}': remaining_balances,
        f'Equity for {name}': equitys,
    }

    return pd.DataFrame(output_data)

# def mortgage_schedule(property_price, deposit, mortgage_term, interest_rate):
#
#     borrowed_capital = property_price - deposit
#     monthly_interest_rate = interest_rate / 12
#     number_of_payments = mortgage_term * 12
#
#     monthly_payment = (borrowed_capital * monthly_interest_rate) / (
#                 1 - (1 + monthly_interest_rate) ** -number_of_payments)
#
#     months = list(range(1, number_of_payments + 1))
#     payments = []
#     interest_payments = []
#     principal_payments = []
#     remaining_balances = []
#
#     remaining_balance = borrowed_capital
#
#     for month in months:
#         interest_payment = remaining_balance * monthly_interest_rate
#         principal_payment = monthly_payment - interest_payment
#         remaining_balance -= principal_payment
#
#         payments.append(monthly_payment)
#         interest_payments.append(interest_payment)
#         principal_payments.append(principal_payment)
#         remaining_balances.append(remaining_balance)
#
#     data = {
#         "Month": months,
#         "Payment": payments,
#         "Interest Payment": interest_payments,
#         "Principal Payment": principal_payments,
#         "Remaining Balance": remaining_balances
#     }
#
#     mortgage_df = pd.DataFrame(data)
#     return mortgage_df

def create_stock_output_df(name, appreciation_rate, investment_amount, acquisition_month, months_buying_stock, sale, sale_month):
    if sale:
        ownership_months = sale_month - acquisition_month
    else:
        ownership_months = 1200  # 100 years

    stock_price = 1000
    owned_stock_amount = 0
    monthly_appreciation_rate = (appreciation_rate / 100) / 12

    stock_prices = []
    owned_stock_amounts = []
    monthly_investment_amounts = []
    monthly_action = []
    stock_values = []

    for month in range(acquisition_month):
        stock_prices.append(0)
        owned_stock_amounts.append(0)
        monthly_investment_amounts.append(0)
        monthly_action.append(0)
        stock_values.append(0)

    for month in range(ownership_months):
        stock_prices.append(stock_price)
        if month < months_buying_stock:
            owned_stock_amount += investment_amount/stock_price
            owned_stock_amounts.append(owned_stock_amount)
            monthly_investment_amounts.append(investment_amount)
            monthly_action.append(1)
        elif month == ownership_months - 1:
            owned_stock_amount = 0
            owned_stock_amounts.append(owned_stock_amount)
            monthly_investment_amounts.append(0)
            monthly_action.append(-1)
        else:
            owned_stock_amounts.append(owned_stock_amount)
            monthly_investment_amounts.append(0)
            monthly_action.append(0)

        stock_values.append(owned_stock_amount * stock_price)
        stock_price += stock_price * monthly_appreciation_rate

    output_data = {
        f'Stock Price for {name}': stock_prices,
        f'Number of Shares for {name}': owned_stock_amount,
        f'Investment Amount for {name}': monthly_investment_amounts,
        f'Action for {name}': monthly_action,
        f'Cash Value for {name}': stock_values,
    }

    return pd.DataFrame(output_data)

def create_savings_output_df(name, asset_value, acquisition_month):
    asset_values = []
    for month in range(acquisition_month):
        asset_values.append(0)

    asset_values.append(asset_value)

    for month in range(1200 - (acquisition_month + 1)):
        asset_values.append(0)

    output_data = {
        f'Asset Value for {name}': asset_values,

    }

    return pd.DataFrame(output_data)



