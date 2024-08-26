import streamlit as st
import pandas as pd

def display_salary_sidebar(update_combined_df):
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
                handle_salary_edit(i, salary_data, update_combined_df)

            if st.button("Delete", key=f"delete_salary_{i}"):
                del st.session_state.salary_dfs[i]
                update_combined_df()
                st.session_state.editing_salary_index = None
                break  # Exit loop after deletion to prevent index errors

def display_expense_sidebar(update_combined_df):
    st.sidebar.header("Your Expenses")
    for i, expense_data in enumerate(st.session_state.expenses_dfs):
        with st.sidebar.expander(expense_data['name'], expanded=False):
            st.write(f"Monthly Expenses: {expense_data['monthly_expense']}")
            st.write(f"Months: {expense_data['months']}")

            if st.button("Edit", key=f"edit_expense_{i}"):
                st.session_state.editing_expense_index = i

            if st.session_state.editing_expense_index == i:
                handle_expense_edit(i, expense_data, update_combined_df)

            if st.button("Delete", key=f"delete_expense_{i}"):
                del st.session_state.expenses_dfs[i]
                update_combined_df()
                st.session_state.editing_expense_index = None
                break  # Exit loop after deletion to prevent index errors

def handle_salary_edit(index, salary_data, update_combined_df):
    # Check if the form is already open for editing
    if st.session_state.editing_salary_index == index:
        new_name = st.text_input("Salary Name", value=salary_data['name'])
        new_annual_income = st.number_input("Annual Gross Income", value=salary_data['annual_income'])
        new_pension_contrib = st.number_input("Pension Contribution (%)", value=salary_data['pension_contrib'])
        new_company_match = st.number_input("Company Match (%)", value=salary_data['company_match'])
        new_num_months = st.number_input("Number of Months", value=salary_data['num_months'], min_value=1, max_value=120)

        if st.button("Save Changes", key=f"save_salary_{index}"):
            st.session_state.salary_dfs[index]['name'] = new_name
            st.session_state.salary_dfs[index]['annual_income'] = new_annual_income
            st.session_state.salary_dfs[index]['pension_contrib'] = new_pension_contrib
            st.session_state.salary_dfs[index]['company_match'] = new_company_match
            st.session_state.salary_dfs[index]['num_months'] = new_num_months

            # Recreate the salary output dataframe with the new values
            new_output_df = create_salary_output_df(new_annual_income, new_pension_contrib, new_company_match, new_num_months)
            st.session_state.salary_dfs[index]['output_df'] = new_output_df

            update_combined_df()  # Update the combined salary dataframe with the new changes
            st.session_state.editing_salary_index = None

        if st.button("Cancel", key=f"cancel_edit_salary_{index}"):
            st.session_state.editing_salary_index = None

def handle_expense_edit(index, expense_data, update_combined_df):
    # Check if the form is already open for editing
    if st.session_state.editing_expense_index == index:
        new_name = st.text_input("Expense Name", value=expense_data['name'])
        new_monthly_expense = st.number_input("Monthly Expenses", value=expense_data['monthly_expense'])
        new_months = st.number_input("Months", value=expense_data['months'], min_value=1, max_value=120)

        if st.button("Save Changes", key=f"save_expense_{index}"):
            st.session_state.expenses_dfs[index]['name'] = new_name
            st.session_state.expenses_dfs[index]['monthly_expense'] = new_monthly_expense
            st.session_state.expenses_dfs[index]['months'] = new_months

            # Recreate the expense output dataframe with the new values
            new_output_df = create_expense_output_df(new_monthly_expense, new_months)
            st.session_state.expenses_dfs[index]['output_df'] = new_output_df

            update_combined_df()  # Update the combined expense dataframe with the new changes
            st.session_state.editing_expense_index = None

        if st.button("Cancel", key=f"cancel_edit_expense_{index}"):
            st.session_state.editing_expense_index = None

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
