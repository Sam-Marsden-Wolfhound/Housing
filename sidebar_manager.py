import streamlit as st
import pandas as pd
from form_handlers import handle_salary_edit, handle_expense_edit, handle_house_edit, handle_rent_edit, handle_stock_edit, handle_asset_edit

def display_refresh_sidebar_button():
    if st.sidebar.button("Refresh Sidebar", key="refresh_sidebar_button"):
        st.session_state.editing_salary_index = None
        st.session_state.editing_expense_index = None


def display_salary_sidebar(state_manager):
    display_refresh_sidebar_button()  # Add the Refresh Sidebar button at the top with a unique key
    st.sidebar.header("Your Salaries")

    for i, salary_data in enumerate(state_manager.get_salary_dfs()):
        with st.sidebar.expander(salary_data['name'], expanded=False):
            st.write(f"Annual Income: {salary_data['annual_income']}")
            st.write(f"Pension Contribution (%): {salary_data['pension_contrib']}")
            st.write(f"Company Match (%): {salary_data['company_match']}")
            st.write(f"Number of Months: {salary_data['num_months']}")

            if st.button("Edit", key=f"edit_salary_{i}"):
                state_manager.set_editing_index(
                    key='editing_salary_index',
                    value=i
                )
            print('val', state_manager.get_editing_index(key='editing_salary_index'), i)
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


def display_housing_sidebar(output_df_handler, update_combined_df, update_joint_combined_df):
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
                handle_house_edit(i, house_data, update_combined_df, output_df_handler, update_joint_combined_df)

            if st.button("Delete", key=f"delete_house_{i}"):
                del st.session_state.housing_dfs[i]
                update_combined_df()
                st.session_state.editing_house_index = None
                break  # Exit loop after deletion to prevent index errors

def display_rent_sidebar(output_df_handler, update_combined_df, update_joint_combined_df):
    """Displays the rent widgets in the sidebar."""
    st.sidebar.header("Your Rents")

    for i, rent_data in enumerate(st.session_state.rent_dfs):
        with st.sidebar.expander(f"{rent_data['name']}"):
            st.write(f"Rent Amount: ${rent_data['rent_amount']}")
            st.write(f"Starting Month: {rent_data['start_month']}")
            st.write(f"Duration: {rent_data['duration']}")

            if st.button("Edit", key=f"edit_rent_{i}"):
                st.session_state.editing_rent_index = i

            if st.session_state.editing_rent_index == i:
                handle_rent_edit(i, rent_data, update_combined_df, output_df_handler, update_joint_combined_df)

            if st.button("Delete", key=f"delete_rent_{i}"):
                del st.session_state.rent_dfs[i]
                update_combined_df()
                st.session_state.editing_rent_index = None
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

def display_asset_sidebar(output_df_handler, update_combined_df):
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


