import pandas as pd
import streamlit as st

class SalaryUI:
    def __init__(self):
        if 'salary_dfs' not in st.session_state:
            st.session_state.salary_dfs = []  # Initialize an empty list for salary dataframes
        if 'editing_index' not in st.session_state:
            st.session_state.editing_index = None  # Track the index of the salary being edited
        if 'next_salary_id' not in st.session_state:
            st.session_state.next_salary_id = 1  # Track the next default salary ID

    def display(self):
        self.salary_input_form()
        self.salary_sidebar()

    def salary_input_form(self):
        st.header("Add New Salary")
        with st.form(key='salary_form', clear_on_submit=True):
            default_name = f"Salary {st.session_state.next_salary_id}"
            name = st.text_input("Salary Name", value=default_name)
            annual_gross_income = st.number_input("Annual Gross Income", value=60000.0)
            pension_contrib = st.number_input("Pension Contribution (%)", value=3.0)
            company_match = st.number_input("Company Match (%)", value=3.0)
            num_months = st.number_input("Number of Months", min_value=1, max_value=120, value=12)
            submitted = st.form_submit_button("Save Salary")

            if submitted:
                input_df, output_df = self.create_salary_df(name, annual_gross_income, pension_contrib, company_match, num_months)
                st.session_state.salary_dfs.append({
                    'name': name,
                    'input_df': input_df,
                    'output_df': output_df,
                    'annual_gross_income': annual_gross_income,
                    'pension_contrib': pension_contrib,
                    'company_match': company_match,
                    'num_months': num_months
                })
                st.session_state.next_salary_id += 1  # Increment the default salary ID for the next salary
                st.success(f"Salary '{name}' added successfully!")

    def create_salary_df(self, name, annual_gross_income, pension_contrib, company_match, num_months):
        # Create salary_input_dataframe
        input_data = {
            'Name': [name],
            'Annual Gross Income': [annual_gross_income],
            'Pension Contribution (%)': [pension_contrib],
            'Company Match (%)': [company_match],
            'Number of Months': [num_months],
        }
        input_df = pd.DataFrame(input_data)

        # Calculate monthly amounts
        monthly_salary = annual_gross_income / 12
        pension_deduction = monthly_salary * (pension_contrib / 100)
        company_pension_contribution = monthly_salary * (company_match / 100)
        combined_pension_contribution = pension_deduction + company_pension_contribution
        tax = monthly_salary * 0.2  # Assuming a flat 20% tax rate
        national_insurance = monthly_salary * 0.12  # Assuming a flat 12% NI rate
        take_home_pay = monthly_salary - pension_deduction - tax - national_insurance

        # Create salary_output_dataframe
        output_data = {
            'Monthly Salary': [monthly_salary] * num_months,
            'Pension Deduction': [pension_deduction] * num_months,
            'Tax': [tax] * num_months,
            'National Insurance': [national_insurance] * num_months,
            'Combined Pension Contribution': [combined_pension_contribution] * num_months,
            'Take Home Pay': [take_home_pay] * num_months,
        }
        output_df = pd.DataFrame(output_data)

        return input_df, output_df

    def salary_sidebar(self):
        st.sidebar.header("Your Salaries")

        # Add a refresh button at the top of the sidebar
        if st.sidebar.button("Refresh Sidebar"):
            st.write(
                """
                <script>
                location.reload();
                </script>
                """,
                unsafe_allow_html=True
            )

        # Track if a deletion has occurred
        deletion_occurred = False

        # Display each salary in the sidebar
        for i in range(len(st.session_state.salary_dfs)):
            if deletion_occurred:
                break  # Stop further processing if a deletion has already occurred

            salary_data = st.session_state.salary_dfs[i]
            with st.sidebar.expander(salary_data['name'], expanded=False):
                if st.session_state.editing_index == i:
                    # Edit mode
                    new_name = st.text_input("Salary Name", value=salary_data['name'], key=f"name_{i}")
                    new_annual_gross_income = st.number_input("Annual Gross Income", value=salary_data['annual_gross_income'], key=f"agi_{i}")
                    new_pension_contrib = st.number_input("Pension Contribution (%)", value=salary_data['pension_contrib'], key=f"pension_{i}")
                    new_company_match = st.number_input("Company Match (%)", value=salary_data['company_match'], key=f"match_{i}")
                    new_num_months = st.number_input("Number of Months", min_value=1, max_value=120, value=salary_data['num_months'], key=f"months_{i}")

                    if st.button("Save", key=f"save_{i}"):
                        input_df, output_df = self.create_salary_df(new_name, new_annual_gross_income, new_pension_contrib, new_company_match, new_num_months)
                        st.session_state.salary_dfs[i] = {
                            'name': new_name,
                            'input_df': input_df,
                            'output_df': output_df,
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

                # Delete button
                if st.button("Delete", key=f"delete_{i}"):
                    del st.session_state.salary_dfs[i]
                    st.session_state.editing_index = None  # Reset editing index
                    deletion_occurred = True  # Set the flag to indicate deletion has occurred

                    # Trigger a page reload using JavaScript to refresh the sidebar
                    st.write(
                        """
                        <script>
                        location.reload();
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                    break  # Exit loop to prevent further processing after deletion

        # Optionally, if you want to display the combined DataFrame and plot after deletion, you can call the methods here
        self.combined_salary_df()
        self.plot_salary_data()

    def combined_salary_df(self):
        if len(st.session_state.salary_dfs) > 0:
            # Combine the salary_output_df from each salary in the order they appear in the sidebar
            combined_df = pd.concat([salary['output_df'] for salary in st.session_state.salary_dfs], ignore_index=True)
            st.dataframe(combined_df)
        else:
            st.write("No salaries added yet.")

    def plot_salary_data(self):
        if len(st.session_state.salary_dfs) > 0:
            # Combine the salary_output_df from each salary in the order they appear in the sidebar
            combined_df = pd.concat([salary['output_df'] for salary in st.session_state.salary_dfs], ignore_index=True)

            # Default selection for the graph
            default_selection = ["Monthly Salary"] if "Monthly Salary" in combined_df.columns else []

            # Select columns to plot with "Monthly Salary" selected by default
            columns_to_plot = st.multiselect("Select columns to plot", combined_df.columns.tolist(),
                                             default=default_selection)

            if columns_to_plot:
                # Plot the selected columns using the index as the x-axis
                st.line_chart(combined_df[columns_to_plot].reset_index(drop=True))

        else:
            st.write("No data available to plot.")


class ExpensesUI:
    def __init__(self):
        if 'expenses_dfs' not in st.session_state:
            st.session_state.expenses_dfs = []  # Initialize an empty list for expense dataframes
        if 'next_expense_id' not in st.session_state:
            st.session_state.next_expense_id = 1  # Track the next default expense ID
        if 'editing_expense_index' not in st.session_state:
            st.session_state.editing_expense_index = None  # Track the index of the expense being edited

    def display(self):
        self.expenses_input_form()
        self.expenses_sidebar()

    def expenses_input_form(self):
        st.header("Add New Expense")
        with st.form(key='expense_form', clear_on_submit=True):
            default_name = f"Expense {st.session_state.next_expense_id}"
            name = st.text_input("Name", value=default_name)
            monthly_expense = st.number_input("Monthly Expenses", value=1000.00)
            months = st.number_input("Months", min_value=1, max_value=120, value=12)
            submitted = st.form_submit_button("Save Expense")

            if submitted:
                input_df = self.create_expense_df(name, monthly_expense, months)
                st.session_state.expenses_dfs.append({
                    'name': name,
                    'input_df': input_df,
                    'monthly_expense': monthly_expense,
                    'months': months
                })
                st.session_state.next_expense_id += 1  # Increment the default expense ID for the next expense
                st.success(f"Expense '{name}' added successfully!")

    def create_expense_df(self, name, monthly_expense, months):
        # Create expense_inputs_dataframe
        input_data = {
            'Name': [name],
            'Monthly Expenses': [monthly_expense],
            'Months': [months],
        }
        return pd.DataFrame(input_data)

    def expenses_sidebar(self):
        st.sidebar.header("Your Expenses")

        # Add a refresh button at the top of the sidebar with a unique key
        if st.sidebar.button("Refresh Sidebar", key="refresh_expenses_sidebar"):
            st.experimental_rerun()  # Use this to re-render the app when the button is clicked

        # Track if a deletion has occurred
        deletion_occurred = False

        # Display each expense in the sidebar
        for i in range(len(st.session_state.expenses_dfs)):
            if deletion_occurred:
                break  # Stop further processing if a deletion has already occurred

            expense_data = st.session_state.expenses_dfs[i]
            with st.sidebar.expander(expense_data['name'], expanded=False):
                if st.session_state.editing_expense_index == i:
                    # Edit mode
                    new_name = st.text_input("Name", value=expense_data['name'], key=f"expense_name_{i}")
                    new_monthly_expense = st.number_input("Monthly Expenses", value=expense_data['monthly_expense'], key=f"expense_amount_{i}")
                    new_months = st.number_input("Months", min_value=1, max_value=120, value=expense_data['months'], key=f"expense_months_{i}")

                    if st.button("Save", key=f"save_expense_{i}"):
                        input_df = self.create_expense_df(new_name, new_monthly_expense, new_months)
                        st.session_state.expenses_dfs[i] = {
                            'name': new_name,
                            'input_df': input_df,
                            'monthly_expense': new_monthly_expense,
                            'months': new_months
                        }
                        st.session_state.editing_expense_index = None
                        st.success(f"Expense '{new_name}' updated successfully!")

                    if st.button("Cancel", key=f"cancel_expense_{i}"):
                        st.session_state.editing_expense_index = None

                else:
                    # View mode
                    st.write(f"Monthly Expenses: {expense_data['monthly_expense']}")
                    st.write(f"Months: {expense_data['months']}")

                    if st.button("Edit", key=f"edit_expense_{i}"):
                        st.session_state.editing_expense_index = i

                # Delete button with a unique key
                if st.button("Delete", key=f"delete_expense_{i}"):
                    del st.session_state.expenses_dfs[i]
                    st.session_state.editing_expense_index = None  # Reset editing index
                    deletion_occurred = True  # Set the flag to indicate deletion has occurred

                    # Trigger a page reload using JavaScript to refresh the sidebar
                    st.write(
                        """
                        <script>
                        location.reload();
                        </script>
                        """,
                        unsafe_allow_html=True
                    )
                    break  # Exit loop to prevent further processing after deletion


