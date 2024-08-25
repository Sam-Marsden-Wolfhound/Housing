import streamlit as st
import pandas as pd

class SalaryUI:
    def __init__(self):
        if 'salary_dfs' not in st.session_state:
            st.session_state.salary_dfs = []  # Initialize an empty list for salary dataframes
        if 'editing_index' not in st.session_state:
            st.session_state.editing_index = None  # Track the index of the salary being edited

    def display(self):
        self.salary_input_form()
        self.salary_sidebar()

    def salary_input_form(self):
        st.header("Add New Salary")
        with st.form(key='salary_form', clear_on_submit=True):
            name = st.text_input("Salary Name", value=f"Salary {len(st.session_state.salary_dfs) + 1}")
            annual_gross_income = st.number_input("Annual Gross Income", value=60000.0)
            pension_contrib = st.number_input("Pension Contribution (%)", value=3.0)
            company_match = st.number_input("Company Match (%)", value=3.0)
            num_months = st.number_input("Number of Months", min_value=1, max_value=120, value=12)
            submitted = st.form_submit_button("Save Salary")

            if submitted:
                df = self.create_salary_df(name, annual_gross_income, pension_contrib, company_match, num_months)
                st.session_state.salary_dfs.append({
                    'name': name,
                    'df': df,
                    'annual_gross_income': annual_gross_income,
                    'pension_contrib': pension_contrib,
                    'company_match': company_match,
                    'num_months': num_months
                })  # Append the data to the list
                st.success(f"Salary '{name}' added successfully!")

    def create_salary_df(self, name, annual_gross_income, pension_contrib, company_match, num_months):
        data = {
            'Month': range(1, num_months + 1),
            'Gross Income': [annual_gross_income / num_months] * num_months,
            'Pension Contribution': [annual_gross_income * (pension_contrib / 100) / num_months] * num_months,
            'Company Match': [annual_gross_income * (company_match / 100) / num_months] * num_months,
        }
        df = pd.DataFrame(data)
        df.name = name
        return df

    def salary_sidebar(self):
        st.sidebar.header("Salaries")
        if not st.session_state.salary_dfs:
            st.sidebar.write("No salaries added yet.")
        else:
            for i, salary_data in enumerate(st.session_state.salary_dfs):
                with st.sidebar.expander(f"{salary_data['name']}"):
                    if st.session_state.editing_index == i:
                        # Editing mode
                        new_name = st.text_input("Salary Name", value=salary_data['name'], key=f"name_{i}")
                        new_annual_gross_income = st.number_input("Annual Gross Income", value=salary_data['annual_gross_income'], key=f"agi_{i}")
                        new_pension_contrib = st.number_input("Pension Contribution (%)", value=salary_data['pension_contrib'], key=f"pension_{i}")
                        new_company_match = st.number_input("Company Match (%)", value=salary_data['company_match'], key=f"match_{i}")
                        new_num_months = st.number_input("Number of Months", min_value=1, max_value=120, value=salary_data['num_months'], key=f"months_{i}")

                        if st.button("Save", key=f"save_{i}"):
                            st.session_state.salary_dfs[i] = {
                                'name': new_name,
                                'df': self.create_salary_df(new_name, new_annual_gross_income, new_pension_contrib, new_company_match, new_num_months),
                                'annual_gross_income': new_annual_gross_income,
                                'pension_contrib': new_pension_contrib,
                                'company_match': new_company_match,
                                'num_months': new_num_months
                            }
                            st.session_state.editing_index = None
                            st.success(f"Salary '{new_name}' updated successfully!")

                        if st.button("Cancel", key=f"cancel_{i}"):
                            st.session_state.editing_index = None

                    else:
                        # View mode
                        st.write(f"Annual Gross Income: {salary_data['annual_gross_income']}")
                        st.write(f"Pension Contribution (%): {salary_data['pension_contrib']}")
                        st.write(f"Company Match (%): {salary_data['company_match']}")
                        st.write(f"Number of Months: {salary_data['num_months']}")

                        if st.button("Edit", key=f"edit_{i}"):
                            st.session_state.editing_index = i
