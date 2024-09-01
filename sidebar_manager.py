import streamlit as st
import pandas as pd

def display_refresh_sidebar_button():
    if st.sidebar.button("Refresh Sidebar", key="refresh_sidebar_button"):
        st.session_state.editing_salary_index = None
        st.session_state.editing_expense_index = None


def display_salary_sidebar(output_df_handler, update_combined_df):
    display_refresh_sidebar_button()  # Add the Refresh Sidebar button at the top with a unique key
    st.sidebar.header("Your Salaries")

    for i, salary_data in enumerate(st.session_state.salary_dfs):
        with st.sidebar.expander(salary_data['name'], expanded=False):
            st.write(f"Annual Income: {salary_data['annual_income']}")
            st.write(f"Pension Contribution (%): {salary_data['pension_contrib']}")
            st.write(f"Company Match (%): {salary_data['company_match']}")
            st.write(f"Number of Months: {salary_data['num_months']}")

            if st.button("Edit", key=f"edit_salary_{i}"):
                st.session_state.editing_salary_index = i

            if st.session_state.editing_salary_index == i:
                handle_salary_edit(i, salary_data, update_combined_df, output_df_handler)

            if st.button("Delete", key=f"delete_salary_{i}"):
                del st.session_state.salary_dfs[i]
                update_combined_df()
                st.session_state.editing_salary_index = None
                break  # Exit loop after deletion to prevent index errors


def display_expense_sidebar(output_df_handler, update_combined_df):
    st.sidebar.header("Your Expenses")

    for i, expense_data in enumerate(st.session_state.expenses_dfs):
        with st.sidebar.expander(expense_data['name'], expanded=False):
            st.write(f"Monthly Expenses: {expense_data['monthly_expense']}")
            st.write(f"Months: {expense_data['months']}")

            if st.button("Edit", key=f"edit_expense_{i}"):
                st.session_state.editing_expense_index = i

            if st.session_state.editing_expense_index == i:
                handle_expense_edit(i, expense_data, update_combined_df, output_df_handler)

            if st.button("Delete", key=f"delete_expense_{i}"):
                del st.session_state.expenses_dfs[i]
                update_combined_df()
                st.session_state.editing_expense_index = None
                break  # Exit loop after deletion to prevent index errors


def display_housing_sidebar(output_df_handler, update_combined_df):
    """Displays the housing widgets in the sidebar."""
    st.sidebar.header("Your Houses")

    for i, house_data in enumerate(st.session_state.housing_dfs):
        with st.sidebar.expander(f"{house_data['name']}"):
            st.write(f"House Value: ${house_data['house_value']}")
            st.write(f"Month of Acquisition: {house_data['acquisition_month']}")
            st.write(f"Appreciation Rate (%): {house_data['appreciation_rate']}%")
            if house_data["mortgage"]:
                st.write(f"Deposit: ${house_data['deposit']}")
                st.write(f"Mortgage Term: {house_data['mortgage_term']} years")
                st.write(f"Interest Rate: {house_data['interest_rate']}%")
            else:
                st.write(f"No Mortgage")
            if house_data["sale"]:
                st.write(f"Month of Sale: {house_data['sale_month']}")

            if st.button("Edit", key=f"edit_house_{i}"):
                st.session_state.editing_house_index = i

            if st.session_state.editing_house_index == i:
                handle_house_edit(i, house_data, update_combined_df, output_df_handler)

            if st.button("Delete", key=f"delete_house_{i}"):
                del st.session_state.housing_dfs[i]
                update_combined_df()
                st.session_state.editing_house_index = None
                break  # Exit loop after deletion to prevent index errors

def display_rent_sidebar(output_df_handler, update_combined_df):
    """Displays the housing widgets in the sidebar."""
    st.sidebar.header("Your Houses")

    for i, house_data in enumerate(st.session_state.housing_dfs):
        with st.sidebar.expander(f"{house_data['name']}"):
            st.write(f"House Value: ${house_data['house_value']}")
            st.write(f"Month of Acquisition: {house_data['acquisition_month']}")
            st.write(f"Appreciation Rate (%): {house_data['appreciation_rate']}%")


            if st.button("Edit", key=f"edit_house_{i}"):
                st.session_state.editing_house_index = i

            if st.session_state.editing_house_index == i:
                handle_house_edit(i, house_data, update_combined_df, output_df_handler)

            if st.button("Delete", key=f"delete_house_{i}"):
                del st.session_state.housing_dfs[i]
                update_combined_df()
                st.session_state.editing_house_index = None
                break  # Exit loop after deletion to prevent index errors


def display_stock_sidebar(output_df_handler, update_combined_df):
    """Displays the housing widgets in the sidebar."""
    st.sidebar.header("Your Stocks")

    for i, stock_data in enumerate(st.session_state.stock_dfs):
        with st.sidebar.expander(stock_data['name'], expanded=False):
            st.write(f"Acquisition Month: {stock_data['acquisition_month']}")
            st.write(f"Dollar-Cost Averaging Amount (£): {stock_data['investment_amount']}")
            st.write(f"Dollar-Cost Averaging Months: {stock_data['months_buying_stock']}")
            st.write(f"Appreciation Rate (%): {stock_data['appreciation_rate']}")
            if stock_data['sale']:
                st.write(f"Month of Sale: {stock_data['sale_month']}")
            else:
                st.write("Hold Stock")

            if st.button("Edit", key=f"edit_stock_{i}"):
                st.session_state.editing_stock_index = i

            if st.session_state.editing_stock_index == i:
                handle_stock_edit(i, stock_data, update_combined_df, output_df_handler)

            if st.button("Delete", key=f"delete_stock_{i}"):
                del st.session_state.stock_dfs[i]
                # update_combined_df()
                st.session_state.editing_stock_index = None
                break  # Exit loop after deletion to prevent index errors

def display_savings_sidebar(output_df_handler, update_combined_df):
    """Displays the housing widgets in the sidebar."""
    st.sidebar.header("Your Savings")

    for i, savings_data in enumerate(st.session_state.savings_dfs):
        with st.sidebar.expander(savings_data['name'], expanded=False):
            st.write(f"Asset Value: {savings_data['asset_value']}")
            st.write(f"Acquisition Month: {savings_data['acquisition_month']}")

            if st.button("Edit", key=f"edit_savings_{i}"):
                st.session_state.editing_savings_index = i

            if st.session_state.editing_savings_index == i:
                handle_savings_edit(i, savings_data, update_combined_df, output_df_handler)

            if st.button("Delete", key=f"delete_savings_{i}"):
                del st.session_state.savings_dfs[i]
                update_combined_df()
                st.session_state.editing_savings_index = None
                break  # Exit loop after deletion to prevent index errors



def handle_salary_edit(index, salary_data, update_combined_df, output_df_handler):
    if st.session_state.editing_salary_index == index:
        new_name = st.text_input("Salary Name", value=salary_data['name'])
        new_annual_income = st.number_input("Annual Gross Income", value=salary_data['annual_income'])
        new_pension_contrib = st.number_input("Pension Contribution (%)", value=salary_data['pension_contrib'])
        new_company_match = st.number_input("Company Match (%)", value=salary_data['company_match'])
        new_num_months = st.number_input("Number of Months", value=salary_data['num_months'], min_value=1,
                                         max_value=120)

        if st.button("Save Changes", key=f"save_salary_{index}"):
            st.session_state.salary_dfs[index]['name'] = new_name
            st.session_state.salary_dfs[index]['annual_income'] = new_annual_income
            st.session_state.salary_dfs[index]['pension_contrib'] = new_pension_contrib
            st.session_state.salary_dfs[index]['company_match'] = new_company_match
            st.session_state.salary_dfs[index]['num_months'] = new_num_months

            # Recreate the salary output dataframe with the new values
            new_output_df = output_df_handler(new_annual_income, new_pension_contrib, new_company_match,
                                                    new_num_months)
            st.session_state.salary_dfs[index]['output_df'] = new_output_df

            update_combined_df()  # Update the combined salary dataframe with the new changes
            st.session_state.editing_salary_index = None

        if st.button("Cancel", key=f"cancel_edit_salary_{index}"):
            st.session_state.editing_salary_index = None


def handle_expense_edit(index, expense_data, update_combined_df, output_df_handler):
    if st.session_state.editing_expense_index == index:
        new_name = st.text_input("Expense Name", value=expense_data['name'])
        new_monthly_expense = st.number_input("Monthly Expenses", value=expense_data['monthly_expense'])
        new_months = st.number_input("Months", value=expense_data['months'], min_value=1, max_value=120)

        if st.button("Save Changes", key=f"save_expense_{index}"):
            st.session_state.expenses_dfs[index]['name'] = new_name
            st.session_state.expenses_dfs[index]['monthly_expense'] = new_monthly_expense
            st.session_state.expenses_dfs[index]['months'] = new_months

            # Recreate the expense output dataframe with the new values
            new_output_df = output_df_handler(new_monthly_expense, new_months)
            st.session_state.expenses_dfs[index]['output_df'] = new_output_df

            update_combined_df()  # Update the combined expense dataframe with the new changes
            st.session_state.editing_expense_index = None

        if st.button("Cancel", key=f"cancel_edit_expense_{index}"):
            st.session_state.editing_expense_index = None

def handle_house_edit(index, house_data, update_combined_df, output_df_handler):
    if st.session_state.editing_house_index == index:
        new_name = st.text_input("House Name", value=house_data['name'])
        new_house_value = st.number_input("House Value", value=house_data['house_value'])
        new_acquisition_month = st.number_input("Month of Acquisition", value=house_data['acquisition_month'])
        new_appreciation_rate = st.number_input("House Appreciation Rate (%)", value=house_data['appreciation_rate'])

        # Mortgage related inputs
        new_mortgage = st.checkbox("Mortgage", value=house_data['mortgage'])
        new_deposit = st.number_input("Deposit", value= house_data['deposit'] if (house_data['deposit'] is not None) else 50000)
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
            st.session_state.housing_dfs[index]['name'] = new_name
            st.session_state.housing_dfs[index]['house_value'] = new_house_value
            st.session_state.housing_dfs[index]['acquisition_month'] = new_acquisition_month
            st.session_state.housing_dfs[index]['appreciation_rate'] = new_appreciation_rate
            st.session_state.housing_dfs[index]['mortgage'] = new_mortgage
            st.session_state.housing_dfs[index]['deposit'] = new_deposit
            st.session_state.housing_dfs[index]['mortgage_term'] = new_mortgage_term
            st.session_state.housing_dfs[index]['interest_rate'] = new_interest_rate
            st.session_state.housing_dfs[index]['sale'] = new_sale
            st.session_state.housing_dfs[index]['sale_month'] = new_sale_month

            # Recreate the housing output dataframe with the new values
            new_output_df = output_df_handler(
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
            st.session_state.housing_dfs[index]['output_df'] = new_output_df

            update_combined_df()  # Update the combined housing dataframe with the new changes
            st.session_state.editing_house_index = None

        if st.button("Cancel", key=f"cancel_edit_expense_{index}"):
            st.session_state.editing_house_index = None

def handle_stock_edit(index, stock_data, update_combined_df, output_df_handler):
    if st.session_state.editing_stock_index == index:

        new_name = st.text_input("Stock Name", value=stock_data['name'])
        new_acquisition_month = st.number_input("Acquisition Month", value=stock_data['acquisition_month'])
        new_investment_amount = st.number_input("Dollar-Cost Averaging Amount (£)", value=stock_data['investment_amount'])
        new_months_buying_stock = st.number_input("Dollar-Cost Averaging Months", value=stock_data['months_buying_stock'])
        new_appreciation_rate = st.number_input("Appreciation Rate (%)", value=stock_data['appreciation_rate'])
        new_sale = st.checkbox("Sell Stock", value=stock_data['sale'])
        new_sale_month = st.number_input("Month of Sale", value=new_acquisition_month + new_months_buying_stock + 1,
                                     min_value=new_acquisition_month + new_months_buying_stock + 1)

        if st.button("Save Changes", key=f"save_stock_{index}"):
            st.session_state.stock_dfs[index]['name'] = new_name
            st.session_state.stock_dfs[index]['acquisition_month'] = new_acquisition_month
            st.session_state.stock_dfs[index]['investment_amount'] = new_investment_amount
            st.session_state.stock_dfs[index]['months_buying_stock'] = new_months_buying_stock
            st.session_state.stock_dfs[index]['appreciation_rate'] = new_appreciation_rate
            st.session_state.stock_dfs[index]['sale'] = new_sale
            st.session_state.stock_dfs[index]['sale_month'] = new_sale_month

            # Recreate the expense output dataframe with the new values
            new_output_df = output_df_handler(new_name, new_appreciation_rate, new_investment_amount, new_acquisition_month, new_months_buying_stock, new_sale, new_sale_month)
            st.session_state.stock_dfs[index]['output_df'] = new_output_df

            update_combined_df()  # Update the combined expense dataframe with the new changes
            st.session_state.editing_stock_index = None

        if st.button("Cancel", key=f"cancel_edit_stock_{index}"):
            st.session_state.editing_stock_index = None

def handle_savings_edit(index, savings_data, update_combined_df, output_df_handler):
    if st.session_state.editing_savings_index == index:
        new_name = st.text_input("Asset Name", value=savings_data['name'])
        new_asset_value = st.number_input("Asset Value", value=savings_data['asset_value'])
        new_acquisition_month = st.number_input("Acquisition Month", value=savings_data['acquisition_month'])

        if st.button("Save Changes", key=f"save_asset_{index}"):
            st.session_state.savings_dfs[index]['name'] = new_name
            st.session_state.savings_dfs[index]['asset_value'] = new_asset_value
            st.session_state.savings_dfs[index]['acquisition_month'] = new_acquisition_month

            output_df = output_df_handler(new_name, new_asset_value, new_acquisition_month)
            st.session_state.savings_dfs[index]['output_df'] = output_df

            update_combined_df()  # Update the combined expense dataframe with the new changes
            st.session_state.editing_savings_index = None

        if st.button("Cancel", key=f"cancel_edit_savings_{index}"):
            st.session_state.editing_savings_index = None

