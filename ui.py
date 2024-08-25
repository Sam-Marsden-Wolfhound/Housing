import streamlit as st

class SalaryUI:
    def __init__(self):
        self.salary_entries = st.session_state.get("salary_entries", [])

    def display(self):
        st.header("Salary Management")
        self.salary_input_form()
        self.salary_sidebar()

    def salary_input_form(self):
        st.subheader("Add New Salary")
        with st.form(key='new_salary_form'):
            name = st.text_input("Salary Name", f"Salary {len(self.salary_entries) + 1}")
            gross_income = st.number_input("Annual Gross Income", value=60000.0)
            pension_contrib = st.number_input("Pension Contribution (%)", value=3)
            company_match = st.number_input("Company Match (%)", value=3)
            num_months = st.number_input("Number of Months", value=12)
            submit_button = st.form_submit_button(label='Save')

            if submit_button:
                new_entry = {
                    "name": name,
                    "gross_income": gross_income,
                    "pension_contrib": pension_contrib,
                    "company_match": company_match,
                    "num_months": num_months,
                }
                self.salary_entries.append(new_entry)
                st.session_state.salary_entries = self.salary_entries
                st.experimental_rerun()

    def salary_sidebar(self):
        st.sidebar.header("Edit Salaries")
        for i, entry in enumerate(self.salary_entries):
            entry_name = entry['name']
            if st.sidebar.button(f"Edit {entry_name}", key=f"edit_{entry_name}"):
                self.edit_salary_entry(i)

    def edit_salary_entry(self, index):
        entry = self.salary_entries[index]
        st.sidebar.header(f"Edit {entry['name']}")
        with st.sidebar.form(key=f'edit_salary_form_{entry["name"]}'):
            entry['name'] = st.text_input("Salary Name", entry['name'])
            entry['gross_income'] = st.number_input("Annual Gross Income", value=entry['gross_income'])
            entry['pension_contrib'] = st.number_input("Pension Contribution (%)", value=entry['pension_contrib'])
            entry['company_match'] = st.number_input("Company Match (%)", value=entry['company_match'])
            entry['num_months'] = st.number_input("Number of Months", value=entry['num_months'])
            submit_button = st.form_submit_button(label='Update')

            if submit_button:
                st.session_state.salary_entries = self.salary_entries
                st.experimental_rerun()

class UI:
    def display(self):
        tabs = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])

        with tabs[0]:
            SalaryUI().display()

        # Placeholder: Implement similar classes for Expenses, Housing, and Analysis.
        with tabs[1]:
            st.header("Expenses Management")
            st.write("Expenses management content goes here.")

        with tabs[2]:
            st.header("Housing Management")
            st.write("Housing management content goes here.")

        with tabs[3]:
            st.header("Analysis")
            st.write("Analysis content goes here.")

if __name__ == "__main__":
    UI().display()
