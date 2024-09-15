import streamlit as st
from data_processing import create_salary_output_df, create_pension_growth_output_df, create_expense_output_df, create_house_output_df, create_rent_output_df, create_stock_output_df, create_asset_output_df


def handle_user_form(state_manager):
    user_age = st.number_input("Age", value=state_manager.get_user_age(), step=1)

    if st.form_submit_button("Update User Info"):
        state_manager.set_user_age(user_age)

        return True
    return False


def handle_salary_form(state_manager):
    # default_name = f"Salary {state_manager.get_form_id(key='next_salary_id')}"
    # Add name check in here, same name will breck Concatenati.
    name = st.text_input("Salary Name", value='Salary')
    annual_income = st.number_input("Annual Gross Income", value=60000, step=1000, format="%d")
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

        st.success('Salary Added')
        state_manager.add_one_to_form_id(key='next_salary_id')
        return True
    return False


def handle_salary_edit(index, salary_data, state_manager):
    new_name = st.text_input("Salary Name", value=salary_data['name'])
    new_annual_income = st.number_input("Annual Gross Income", value=salary_data['annual_income'], format="%d")
    new_pension_contrib = st.number_input("Pension Contribution (%)", value=salary_data['pension_contrib'])
    new_company_match = st.number_input("Company Match (%)", value=salary_data['company_match'])
    new_num_months = st.number_input("Number of Months", value=salary_data['num_months'], min_value=1,
                                     max_value=120)

    if st.button("Save Changes", key=f"save_salary_{index}"):
        state_manager.get_salary_dfs()[index]['name'] = new_name
        state_manager.get_salary_dfs()[index]['annual_income'] = new_annual_income
        state_manager.get_salary_dfs()[index]['pension_contrib'] = new_pension_contrib
        state_manager.get_salary_dfs()[index]['company_match'] = new_company_match
        state_manager.get_salary_dfs()[index]['num_months'] = new_num_months

        # Recreate the salary output dataframe with the new values
        new_output_df = create_salary_output_df(new_annual_income, new_pension_contrib, new_company_match,
                                                new_num_months)
        state_manager.get_salary_dfs()[index]['output_df'] = new_output_df

        state_manager.update_salary_df()  # Update the combined salary dataframe with the new changes
        state_manager.update_analysis_df()

        state_manager.set_editing_index(
            key='editing_salary_index',
            value=None
        )

    if st.button("Cancel", key=f"cancel_edit_salary_{index}"):
        state_manager.set_editing_index(
            key='editing_salary_index',
            value=None
        )

def handle_pension_growth_form(state_manager):
    # default_name = f"Pension {state_manager.get_form_id(key='next_pension_id')}"
    name = st.text_input("Pension Growth Name", value='Pension')
    annual_growth_rate = st.number_input("Annual Growth Rate (%)", value=3.00)
    months = st.number_input("Months", value=12, min_value=1)

    if st.form_submit_button("Add Pension Growth"):
        output_df = create_pension_growth_output_df(annual_growth_rate, months)
        state_manager.add_pension_growth_df({
            'name': name,
            'output_df': output_df,
            'annual_growth_rate': annual_growth_rate,
            'months': months
        })

        st.success('Pension Added')
        state_manager.add_one_to_form_id(key='next_pension_id')
        return True

    return False


def handle_pension_growth_edit(index, pension_data, state_manager):
    new_name = st.text_input("Pension Growth Name", value=pension_data['name'])
    new_annual_growth_rate = st.number_input("Annual Growth Rate (%)", value=pension_data['annual_growth_rate'])
    new_months = st.number_input("Months", value=pension_data['months'], min_value=1, max_value=1200)

    if st.button("Save Changes", key=f"save_pension_{index}"):
        state_manager.get_pension_growth_dfs()[index]['name'] = new_name
        state_manager.get_pension_growth_dfs()[index]['annual_growth_rate'] = new_annual_growth_rate
        state_manager.get_pension_growth_dfs()[index]['months'] = new_months

        # Recreate the pension growth output dataframe with the new values
        new_output_df = create_pension_growth_output_df(new_annual_growth_rate, new_months)
        state_manager.get_pension_growth_dfs()[index]['output_df'] = new_output_df

        state_manager.update_salary_df()
        state_manager.update_analysis_df()

        state_manager.set_editing_index(
            key='editing_pension_index',
            value=None
        )

    if st.button("Cancel", key=f"cancel_edit_pension_{index}"):
        state_manager.set_editing_index(
            key='editing_pension_index',
            value=None
        )


def handle_expense_form(state_manager):
    # default_name = f"Expense {state_manager.get_form_id(key='next_expense_id')}"
    name = st.text_input("Expense Name", value='Expense')
    monthly_expense = st.number_input("Monthly Expenses", value=1000, format="%d")
    months = st.number_input("Months", value=12, min_value=1)

    if st.form_submit_button("Add Expense"):
        output_df = create_expense_output_df(monthly_expense, months)
        state_manager.add_expense_df({
            'name': name,
            'output_df': output_df,
            'monthly_expense': monthly_expense,
            'months': months
        })

        st.success('Expense Added')
        state_manager.add_one_to_form_id(key='next_expense_id')
        return True
    return False


def handle_expense_edit(index, expense_data, state_manager):
    new_name = st.text_input("Expense Name", value=expense_data['name'])
    new_monthly_expense = st.number_input("Monthly Expenses", value=expense_data['monthly_expense'], format="%d")
    new_months = st.number_input("Months", value=expense_data['months'], min_value=1, max_value=1200)

    if st.button("Save Changes", key=f"save_expense_{index}"):
        state_manager.get_expense_dfs()[index]['name'] = new_name
        state_manager.get_expense_dfs()[index]['monthly_expense'] = new_monthly_expense
        state_manager.get_expense_dfs()[index]['months'] = new_months

        # Recreate the expense output dataframe with the new values
        new_output_df = create_expense_output_df(new_monthly_expense, new_months)
        state_manager.get_expense_dfs()[index]['output_df'] = new_output_df

        state_manager.update_expense_df()
        state_manager.update_analysis_df()

        state_manager.set_editing_index(
            key='editing_expense_index',
            value=None
        )

    if st.button("Cancel", key=f"cancel_edit_expense_{index}"):
        state_manager.set_editing_index(
            key='editing_expense_index',
            value=None
        )


def handle_house_form(state_manager):
    """Handles the housing input form and returns the data."""
    st.write("Add a new house")
    # default_name = f"House {state_manager.get_form_id(key='next_house_id')}"
    name = st.text_input("House Name", value='House')
    house_value = st.number_input("House Value", value=200000, format="%d")
    acquisition_month = st.number_input("Month of Acquisition", value=0)
    appreciation_rate = st.number_input("House Appreciation Rate (%)", value=1.50)

    # Mortgage related inputs
    with st.expander("Mortgage Details", expanded=False):
        mortgage = st.checkbox("Mortgage")
        deposit = st.number_input("Deposit", value=50000, format="%d")
        mortgage_term = st.number_input("Mortgage Term (years)", value=25)
        interest_rate = st.number_input("Interest Rate (%)", value=3.50)

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
        output_df = create_house_output_df(
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
        # if 'housing_dfs' not in st.session_state:
        #     st.session_state.housing_dfs = []

        state_manager.add_house_df({
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

        st.success('House Added')
        state_manager.add_one_to_form_id(key='next_house_id')
        return True
    return False


def handle_house_edit(index, house_data, state_manager):
    new_name = st.text_input("House Name", value=house_data['name'])
    new_house_value = st.number_input("House Value", value=house_data['house_value'], format="%d")
    new_acquisition_month = st.number_input("Month of Acquisition", value=house_data['acquisition_month'])
    new_appreciation_rate = st.number_input("House Appreciation Rate (%)", value=house_data['appreciation_rate'])

    # Mortgage related inputs
    new_mortgage = st.checkbox("Mortgage", value=house_data['mortgage'])
    new_deposit = st.number_input("Deposit", value= house_data['deposit'] if (house_data['deposit'] is not None) else 50000, format="%d")
    new_mortgage_term = st.number_input("Mortgage Term (years)", value=house_data['mortgage_term'] if (house_data['mortgage_term'] is not None) else 25)
    new_interest_rate = st.number_input("Interest Rate (%)", value=house_data['interest_rate'] if (house_data['interest_rate'] is not None) else 3.50)
    if new_mortgage:
        pass
    else:
        new_deposit = None
        new_mortgage_term = None
        new_interest_rate = None

    # Sale related inputs
    new_sale = st.checkbox("Sale of House", value=house_data['sale'])
    new_sale_month = st.number_input("Month of Sale", value=new_acquisition_month + 1, min_value=new_acquisition_month + 1)
    if new_sale:
        pass
    else:
        new_sale_month = None

    if st.button("Save Changes", key=f"save_expense_{index}"):
        state_manager.get_house_dfs()[index]['name'] = new_name
        state_manager.get_house_dfs()[index]['house_value'] = new_house_value
        state_manager.get_house_dfs()[index]['acquisition_month'] = new_acquisition_month
        state_manager.get_house_dfs()[index]['appreciation_rate'] = new_appreciation_rate
        state_manager.get_house_dfs()[index]['mortgage'] = new_mortgage
        state_manager.get_house_dfs()[index]['deposit'] = new_deposit
        state_manager.get_house_dfs()[index]['mortgage_term'] = new_mortgage_term
        state_manager.get_house_dfs()[index]['interest_rate'] = new_interest_rate
        state_manager.get_house_dfs()[index]['sale'] = new_sale
        state_manager.get_house_dfs()[index]['sale_month'] = new_sale_month

        # Recreate the housing output dataframe with the new values
        new_output_df = create_house_output_df(
            new_name,
            new_house_value,
            new_acquisition_month,
            new_appreciation_rate,
            new_mortgage,
            new_deposit,
            new_mortgage_term,
            new_interest_rate,
            new_sale,
            new_sale_month
        )
        state_manager.get_house_dfs()[index]['output_df'] = new_output_df

        state_manager.update_house_df()
        state_manager.update_house_and_rent_df()
        state_manager.update_analysis_df()

        state_manager.set_editing_index(
            key='editing_house_index',
            value=None
        )

    if st.button("Cancel", key=f"cancel_edit_expense_{index}"):
        state_manager.set_editing_index(
            key='editing_house_index',
            value=None
        )


def handle_rent_form(state_manager):
    # default_name = f"Rent {state_manager.get_form_id(key='next_rent_id')}"
    name = st.text_input("Rent Name", value='Rent')
    rent_amount = st.number_input("Rent Amount", value=2000, format="%d")
    start_month = st.number_input("Starting Month", value=0)
    duration = st.number_input("Duration", value=12, min_value=0)

    if st.form_submit_button("Add Rent"):
        output_df = create_rent_output_df(name, rent_amount, start_month, duration)

        state_manager.add_rent_df({
            'name': name,
            'rent_amount': rent_amount,
            'start_month': start_month,
            'duration': duration,
            'output_df': output_df,
        })

        st.success('Rent Added')
        state_manager.add_one_to_form_id(key='next_rent_id')
        return True
    return False


def handle_rent_edit(index, rent_data, state_manager):
    new_name = st.text_input("Rent Name", value=rent_data['name'])
    new_rent_amount = st.number_input("Rent Amount", value=rent_data['rent_amount'], format="%d")
    new_start_month = st.number_input("Starting Month", value=rent_data['start_month'])
    new_duration = st.number_input("Duration", value=rent_data['duration'])

    if st.button("Save Changes", key=f"save_rent_{index}"):
        state_manager.get_rent_dfs()[index]['name'] = new_name
        state_manager.get_rent_dfs()[index]['rent_amount'] = new_rent_amount
        state_manager.get_rent_dfs()[index]['start_month'] = new_start_month
        state_manager.get_rent_dfs()[index]['duration'] = new_duration

        # Recreate the expense output dataframe with the new values
        new_output_df = create_rent_output_df(new_name, new_rent_amount, new_start_month, new_duration)
        state_manager.get_rent_dfs()[index]['output_df'] = new_output_df

        state_manager.update_rent_df()
        state_manager.update_house_and_rent_df()
        state_manager.update_analysis_df()

        state_manager.set_editing_index(
            key='editing_rent_index',
            value=None
        )

    if st.button("Cancel", key=f"cancel_edit_rent_{index}"):
        state_manager.set_editing_index(
            key='editing_rent_index',
            value=None
        )


def handle_stock_form(state_manager):
    # default_name = f"Stock {state_manager.get_form_id(key='next_stock_id')}"
    name = st.text_input("Stock Name", value='Stock')
    acquisition_month = st.number_input("Acquisition Month", value=0)
    investment_amount = st.number_input("Dollar-Cost Averaging Amount", value=100, min_value=0, format="%d")
    months_buying_stock = st.number_input("Dollar-Cost Averaging Months", value=60, min_value=0)
    appreciation_rate = st.number_input("Appreciation Rate (%)", value=3.50)
    with st.expander("Sale Details", expanded=False):
        sale = st.checkbox("Sell Stock")
        sale_month = st.number_input("Month of Sale", value=acquisition_month + months_buying_stock + 1, min_value=acquisition_month + months_buying_stock + 1)
    if not sale:
        sale_month = None

    if st.form_submit_button("Add Stock"):
        output_df = create_stock_output_df(name, appreciation_rate, investment_amount, acquisition_month, months_buying_stock, sale, sale_month)

        state_manager.add_stock_df({
            'name': name,
            'acquisition_month': acquisition_month,
            'investment_amount': investment_amount,
            'months_buying_stock': months_buying_stock,
            'appreciation_rate': appreciation_rate,
            'sale': sale,
            'sale_month': sale_month,
            'output_df': output_df,
        })

        st.success('Stock Added')
        state_manager.add_one_to_form_id(key='next_stock_id')
        return True
    return False


def handle_stock_edit(index, stock_data, state_manager):
    new_name = st.text_input("Stock Name", value=stock_data['name'])
    new_acquisition_month = st.number_input("Acquisition Month", value=stock_data['acquisition_month'])
    new_investment_amount = st.number_input("Dollar-Cost Averaging Amount", value=stock_data['investment_amount'], format="%d")
    new_months_buying_stock = st.number_input("Dollar-Cost Averaging Months", value=stock_data['months_buying_stock'])
    new_appreciation_rate = st.number_input("Appreciation Rate (%)", value=stock_data['appreciation_rate'])
    new_sale = st.checkbox("Sell Stock", value=stock_data['sale'])
    new_sale_month = st.number_input("Month of Sale", value=new_acquisition_month + new_months_buying_stock + 1,
                                 min_value=new_acquisition_month + new_months_buying_stock + 1)

    if st.button("Save Changes", key=f"save_stock_{index}"):
        state_manager.get_stock_dfs()[index]['name'] = new_name
        state_manager.get_stock_dfs()[index]['acquisition_month'] = new_acquisition_month
        state_manager.get_stock_dfs()[index]['investment_amount'] = new_investment_amount
        state_manager.get_stock_dfs()[index]['months_buying_stock'] = new_months_buying_stock
        state_manager.get_stock_dfs()[index]['appreciation_rate'] = new_appreciation_rate
        state_manager.get_stock_dfs()[index]['sale'] = new_sale
        state_manager.get_stock_dfs()[index]['sale_month'] = new_sale_month

        # Recreate the expense output dataframe with the new values
        new_output_df = create_stock_output_df(new_name, new_appreciation_rate, new_investment_amount, new_acquisition_month, new_months_buying_stock, new_sale, new_sale_month)
        state_manager.get_stock_dfs()[index]['output_df'] = new_output_df

        state_manager.update_stock_df()
        state_manager.update_analysis_df()

        state_manager.set_editing_index(
            key='editing_stock_index',
            value=None
        )

    if st.button("Cancel", key=f"cancel_edit_stock_{index}"):
        state_manager.set_editing_index(
            key='editing_stock_index',
            value=None
        )


def handle_asset_form(state_manager):
    # default_name = f"Asset {state_manager.get_form_id(key='next_asset_id')}"
    name = st.text_input("Asset Name", value='Asset')
    asset_value = st.number_input("Asset Value", value=1000, format="%d")
    acquisition_month = st.number_input("Acquisition Month", value=0, min_value=0)

    if st.form_submit_button("Add Asset"):
        output_df = create_asset_output_df(name, asset_value, acquisition_month)
        state_manager.add_asset_df({
            'name': name,
            'asset_value': asset_value,
            'acquisition_month': acquisition_month,
            'output_df': output_df,
        })

        st.success('Asset Added')
        state_manager.add_one_to_form_id(key='next_asset_id')
        return True
    return False


def handle_asset_edit(index, savings_data, state_manager):
    new_name = st.text_input("Asset Name", value=savings_data['name'])
    new_asset_value = st.number_input("Asset Value", value=savings_data['asset_value'], format="%d")
    new_acquisition_month = st.number_input("Acquisition Month", value=savings_data['acquisition_month'])

    if st.button("Save Changes", key=f"save_asset_{index}"):
        state_manager.get_asset_dfs()[index]['name'] = new_name
        state_manager.get_asset_dfs()[index]['asset_value'] = new_asset_value
        state_manager.get_asset_dfs()[index]['acquisition_month'] = new_acquisition_month

        output_df = create_asset_output_df(new_name, new_asset_value, new_acquisition_month)
        state_manager.get_asset_dfs()[index]['output_df'] = output_df

        state_manager.update_asset_df()
        state_manager.update_analysis_df()

        state_manager.set_editing_index(
            key='editing_asset_index',
            value=None
        )

    if st.button("Cancel", key=f"cancel_edit_asset_{index}"):
        state_manager.set_editing_index(
            key='editing_asset_index',
            value=None
        )


