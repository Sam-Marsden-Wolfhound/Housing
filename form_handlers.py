import pandas as pd
import streamlit as st


def handle_salary_form():
    default_name = f"Salary {st.session_state.next_salary_id}"
    name = st.text_input("Salary Name", value=default_name)
    annual_income = st.number_input("Annual Gross Income", value=60000)
    pension_contrib = st.number_input("Pension Contribution (%)", value=3.0)
    company_match = st.number_input("Company Match (%)", value=3.0)
    num_months = st.number_input("Number of Months", value=12, min_value=1, max_value=120)

    if st.form_submit_button("Save Salary"):
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

    if st.form_submit_button("Save Expense"):
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
