import streamlit as st
import pandas as pd
from form_handlers import handle_salary_edit, handle_expense_edit, handle_house_edit, handle_rent_edit, handle_stock_edit, handle_asset_edit

def display_refresh_sidebar_button(state_manager):
    if st.sidebar.button("Refresh Page", key="refresh_sidebar_button"):
        # st.session_state.editing_salary_index = None
        # st.session_state.editing_expense_index = None
        state_manager.update_all()


def display_salary_sidebar(state_manager):
    display_refresh_sidebar_button(state_manager)  # Add the Refresh Sidebar button at the top with a unique key
    st.sidebar.header("Your Salaries")

    for i, salary_data in enumerate(state_manager.get_salary_dfs()):
        with st.sidebar.expander(salary_data['name'], expanded=False):
            st.write(f"Annual Income: {'{:,.0f}'.format(salary_data['annual_income'])}")
            st.write(f"Pension Contribution (%): {salary_data['pension_contrib']}")
            st.write(f"Company Match (%): {salary_data['company_match']}")
            # st.write(f"Number of Months: {salary_data['num_months']}")
            st.write(f"Number of: Years {salary_data['num_months'] // 12} - Months {salary_data['num_months'] % 12}")

            if st.button("Edit", key=f"edit_salary_{i}"):
                state_manager.set_editing_index(
                    key='editing_salary_index',
                    value=i
                )

            if state_manager.get_editing_index(key='editing_salary_index') == i:
                handle_salary_edit(i, salary_data, state_manager)

            if st.button("Delete", key=f"delete_salary_{i}"):
                del state_manager.get_salary_dfs()[i]
                state_manager.update_all()
                state_manager.set_editing_index(
                    key='editing_salary_index',
                    value=None
                )
                break  # Exit loop after deletion to prevent index errors


def display_expense_sidebar(state_manager):
    st.sidebar.header("Your Expenses")

    for i, expense_data in enumerate(state_manager.get_expense_dfs()):
        with st.sidebar.expander(expense_data['name'], expanded=False):
            st.write(f"Monthly Expenses: {'{:,.0f}'.format(expense_data['monthly_expense'])}")
            # st.write(f"Months: {expense_data['months']}")
            st.write(f"Number of: Years {expense_data['months'] // 12} - Months {expense_data['months'] % 12}")

            if st.button("Edit", key=f"edit_expense_{i}"):
                state_manager.set_editing_index(
                    key='editing_expense_index',
                    value=i
                )

            if state_manager.get_editing_index(key='editing_expense_index') == i:
                handle_expense_edit(i, expense_data, state_manager)

            if st.button("Delete", key=f"delete_expense_{i}"):
                del state_manager.get_expense_dfs()[i]
                state_manager.update_all()
                state_manager.set_editing_index(
                    key='editing_expense_index',
                    value=None
                )
                break  # Exit loop after deletion to prevent index errors


def display_house_sidebar(state_manager):
    """Displays the housing widgets in the sidebar."""
    st.sidebar.header("Your Houses")

    for i, house_data in enumerate(state_manager.get_house_dfs()):
        with st.sidebar.expander(f"{house_data['name']}"):
            st.write(f"House Value: {'{:,.0f}'.format(house_data['house_value'])}")
            # st.write(f"Month of Acquisition: {house_data['acquisition_month']}")
            st.write(f"Acquisition: Years {house_data['acquisition_month'] // 12} - Months {house_data['acquisition_month'] % 12}")
            st.write(f"Appreciation Rate (%): {house_data['appreciation_rate']}%")
            if house_data["mortgage"]:
                st.write(f"Deposit: {'{:,.0f}'.format(house_data['deposit'])}")
                st.write(f"Mortgage Term: {house_data['mortgage_term']} years")
                st.write(f"Interest Rate: {house_data['interest_rate']}%")
            else:
                st.write(f"No Mortgage")
            if house_data["sale"]:
                # st.write(f"Month of Sale: {house_data['sale_month']}")
                st.write(f"Sale: Years {house_data['sale_month'] // 12} - Months {house_data['sale_month'] % 12}")

            if st.button("Edit", key=f"edit_house_{i}"):
                state_manager.set_editing_index(
                    key='editing_house_index',
                    value=i
                )

            if state_manager.get_editing_index(key='editing_house_index') == i:
                handle_house_edit(i, house_data, state_manager)

            if st.button("Delete", key=f"delete_house_{i}"):
                del state_manager.get_house_dfs()[i]
                state_manager.update_all()
                state_manager.set_editing_index(
                    key='editing_house_index',
                    value=None
                )
                break  # Exit loop after deletion to prevent index errors

def display_rent_sidebar(state_manager):
    """Displays the rent widgets in the sidebar."""
    st.sidebar.header("Your Rents")

    for i, rent_data in enumerate(state_manager.get_rent_dfs()):
        with st.sidebar.expander(f"{rent_data['name']}"):
            st.write(f"Rent Amount: {'{:,.0f}'.format(rent_data['rent_amount'])}")
            # st.write(f"Starting Month: {rent_data['start_month']}")
            st.write(f"Starting: Years {rent_data['start_month'] // 12} - Months {rent_data['start_month'] % 12}")
            # st.write(f"Duration: {rent_data['duration']}")
            st.write(f"Duration: Years {rent_data['duration'] // 12} - Months {rent_data['duration'] % 12}")

            if st.button("Edit", key=f"edit_rent_{i}"):
                state_manager.set_editing_index(
                    key='editing_rent_index',
                    value=i
                )

            if state_manager.get_editing_index(key='editing_rent_index') == i:
                handle_rent_edit(i, rent_data, state_manager)

            if st.button("Delete", key=f"delete_rent_{i}"):
                del state_manager.get_rent_dfs()[i]
                state_manager.update_all()
                state_manager.set_editing_index(
                    key='editing_rent_index',
                    value=None
                )
                break  # Exit loop after deletion to prevent index errors


def display_stock_sidebar(state_manager):
    """Displays the housing widgets in the sidebar."""
    st.sidebar.header("Your Stocks")

    for i, stock_data in enumerate(state_manager.get_stock_dfs()):
        with st.sidebar.expander(stock_data['name'], expanded=False):
            # st.write(f"Acquisition Month: {stock_data['acquisition_month']}")
            st.write(f"Acquisition: Years {stock_data['acquisition_month'] // 12} - Months {stock_data['acquisition_month'] % 12}")
            st.write(f"Dollar-Cost Averaging Amount: {'{:,.0f}'.format(stock_data['investment_amount'])}")
            # st.write(f"Dollar-Cost Averaging Months: {stock_data['months_buying_stock']}")
            st.write(f"Dollar-Cost Averaging: Years {stock_data['months_buying_stock'] // 12} - Months {stock_data['months_buying_stock'] % 12}")

            st.write(f"Appreciation Rate (%): {stock_data['appreciation_rate']}")

            if stock_data['sale']:
                # st.write(f"Month of Sale: {stock_data['sale_month']}")
                st.write(f"Sale: Years {stock_data['sale_month'] // 12} - Months {stock_data['sale_month'] % 12}")

            else:
                st.write("Hold Stock")

            if st.button("Edit", key=f"edit_stock_{i}"):
                state_manager.set_editing_index(
                    key='editing_stock_index',
                    value=i
                )

            if state_manager.get_editing_index(key='editing_stock_index') == i:
                handle_stock_edit(i, stock_data, state_manager)

            if st.button("Delete", key=f"delete_stock_{i}"):
                del state_manager.get_stock_dfs()[i]
                state_manager.update_all()
                state_manager.set_editing_index(
                    key='editing_stock_index',
                    value=None
                )
                break  # Exit loop after deletion to prevent index errors

def display_asset_sidebar(state_manager):
    """Displays the housing widgets in the sidebar."""
    st.sidebar.header("Your Assets")

    for i, savings_data in enumerate(state_manager.get_asset_dfs()):
        with st.sidebar.expander(savings_data['name'], expanded=False):
            st.write(f"Asset Value: {'{:,.0f}'.format(savings_data['asset_value'])}")
            # st.write(f"Acquisition Month: {savings_data['acquisition_month']}")
            st.write(f"Acquisition: Years {savings_data['acquisition_month'] // 12} - Months {savings_data['acquisition_month'] % 12}")

            if st.button("Edit", key=f"edit_asset_{i}"):
                state_manager.set_editing_index(
                    key='editing_asset_index',
                    value=i
                )

            if state_manager.get_editing_index(key='editing_asset_index') == i:
                handle_asset_edit(i, savings_data, state_manager)

            if st.button("Delete", key=f"delete_asset_{i}"):
                del state_manager.get_asset_dfs()[i]
                state_manager.update_all()
                state_manager.set_editing_index(
                    key='editing_asset_index',
                    value=None
                )
                break  # Exit loop after deletion to prevent index errors


