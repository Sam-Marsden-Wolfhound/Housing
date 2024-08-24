import streamlit as st
from dataframe_builder import DataFrameBuilder

class SalaryUI:
    def display(self, df_builder: DataFrameBuilder):
        st.sidebar.header("Add New Salary Entry")
        new_gross_income = st.sidebar.number_input("Gross Annual Income (£)", min_value=10000, max_value=500000,
                                                   value=40000, key="salary_income")
        new_pension_contribution_percent = st.sidebar.slider("Your Pension Contribution (%)", min_value=0, max_value=100,
                                                             value=5, key="salary_pension")
        new_company_match_percent = st.sidebar.slider("Company Pension Match (%)", min_value=0, max_value=100, value=5,
                                                      key="salary_match")
        new_num_months = st.sidebar.number_input("Number of Months", min_value=1, value=12, key="salary_months")
        if st.sidebar.button("Add Salary"):
            df_builder.financial_entry.add_salary(new_gross_income, new_pension_contribution_percent,
                                                  new_company_match_percent, new_num_months)
            st.session_state.df = df_builder.rebuild_dataframe()

        # Salary entries in collapsible sections
        for i, entry in enumerate(df_builder.financial_entry.salary_entries):
            with st.sidebar.expander(f"Salary Entry {i + 1}: £{entry['gross_income']} for {entry['num_months']} months"):
                updated_gross_income = st.number_input(f"Gross Annual Income (£) for Entry {i + 1}",
                                                       min_value=10000, max_value=500000, value=entry['gross_income'],
                                                       key=f"gross_income_{i}")
                updated_pension_contribution_percent = st.slider(f"Your Pension Contribution (%) for Entry {i + 1}",
                                                                 min_value=0, max_value=100,
                                                                 value=entry['pension_contribution_percent'],
                                                                 key=f"pension_{i}")
                updated_company_match_percent = st.slider(f"Company Pension Match (%) for Entry {i + 1}",
                                                          min_value=0, max_value=100, value=entry['company_match_percent'],
                                                          key=f"company_{i}")
                updated_num_months = st.number_input(f"Number of Months for Entry {i + 1}",
                                                     min_value=1, value=entry['num_months'], key=f"num_months_{i}")

                if st.button(f"Save Changes for Entry {i + 1}"):
                    df_builder.financial_entry.salary_entries[i] = {
                        "gross_income": updated_gross_income,
                        "pension_contribution_percent": updated_pension_contribution_percent,
                        "company_match_percent": updated_company_match_percent,
                        "num_months": updated_num_months
                    }
                    st.session_state.df = df_builder.rebuild_dataframe()
                    st.success(f"Updated data for Entry {i + 1}.")

                if st.button(f"Delete Salary Entry {i + 1}"):
                    df_builder.financial_entry.salary_entries.pop(i)
                    st.session_state.df = df_builder.rebuild_dataframe()
                    st.success(f"Deleted data for Entry {i + 1}.")
                    break


class ExpensesUI:
    def display(self, df_builder: DataFrameBuilder):
        st.sidebar.header("Add New Expense Entry")
        new_monthly_expense = st.sidebar.number_input("Monthly Expense (£)", min_value=0, max_value=20000, value=1000,
                                                      key="expense_amount")
        new_expense_num_months = st.sidebar.number_input("Number of Months", min_value=1, value=12,
                                                         key="expense_months")

        if st.sidebar.button("Add Expense"):
            st.session_state.expense_entries.append({
                "monthly_expense": new_monthly_expense,
                "num_months": new_expense_num_months
            })
            st.session_state.df = df_builder.rebuild_dataframe()

        # Expense entries in collapsible sections
        for i, entry in enumerate(st.session_state.expense_entries):
            with st.sidebar.expander(
                    f"Expense Entry {i + 1}: £{entry['monthly_expense']} for {entry['num_months']} months"):
                updated_monthly_expense = st.number_input(f"Monthly Expense (£) for Entry {i + 1}", min_value=0,
                                                          max_value=20000, value=entry['monthly_expense'],
                                                          key=f"monthly_expense_{i}")
                updated_expense_num_months = st.number_input(f"Number of Months for Entry {i + 1}", min_value=1,
                                                             value=entry['num_months'], key=f"expense_num_months_{i}")

                if st.button(f"Save Changes for Expense Entry {i + 1}"):
                    st.session_state.expense_entries[i] = {
                        "monthly_expense": updated_monthly_expense,
                        "num_months": updated_expense_num_months
                    }
                    st.session_state.df = df_builder.rebuild_dataframe()
                    st.success(f"Updated data for Expense Entry {i + 1}.")

                if st.button(f"Delete Expense Entry {i + 1}"):
                    st.session_state.expense_entries.pop(i)
                    st.session_state.df = df_builder.rebuild_dataframe()
                    st.success(f"Deleted data for Expense Entry {i + 1}.")
                    break


class HousingUI:
    def display(self, df_builder: DataFrameBuilder):
        st.sidebar.header("Add New Housing Entry")
        new_house_name = st.sidebar.text_input("House Name", value=f"House {st.session_state.house_counter}",
                                               key="house_name")
        new_house_value = st.sidebar.number_input("House Value (£)", min_value=50000, max_value=2000000, value=300000,
                                                  key="house_value")
        new_month_acquisition = st.sidebar.number_input("Month of Acquisition", min_value=1, value=1,
                                                        key="month_acquisition")
        new_appreciation_rate = st.sidebar.number_input("Yearly Property Appreciation (%)", min_value=0.0, max_value=20.0,
                                                        value=5.0, step=0.1, key="appreciation_rate")
        sale = st.sidebar.checkbox("Sale", key="house_sale")
        new_month_sale = None
        if sale:
            new_month_sale = st.sidebar.number_input("Month of Sale", min_value=new_month_acquisition + 1,
                                                     value=new_month_acquisition + 12, key="month_sale")

        mortgage = st.sidebar.checkbox("Mortgage", key="house_mortgage")
        if mortgage:
            deposit = st.sidebar.number_input("Deposit (£)", min_value=0, max_value=new_house_value, value=30000,
                                              key="deposit")
            mortgage_term = st.sidebar.number_input("Mortgage Term (Years)", min_value=1, max_value=40, value=25,
                                                    key="mortgage_term")
            standard_rate = st.sidebar.number_input("Standard Variable Rate (%)", min_value=0.0, max_value=10.0, value=4.0,
                                                    step=0.1, key="standard_rate")

        if st.sidebar.button("Add House"):
            df_builder.financial_entry.add_house(new_house_name, new_house_value, new_month_acquisition,
                                                 new_appreciation_rate, sale, new_month_sale, mortgage,
                                                 deposit, mortgage_term, standard_rate)
            st.session_state.house_counter += 1
            st.session_state.df = df_builder.rebuild_dataframe()

        # Housing entries in an ordered list
        for i, entry in enumerate(sorted(df_builder.financial_entry.housing_entries, key=lambda x: x["month_acquisition"])):
            with st.sidebar.expander(f"{entry['house_name']} (Acquired Month {entry['month_acquisition']})"):
                updated_house_name = st.text_input("House Name", value=entry['house_name'], key=f"house_name_{i}")
                updated_house_value = st.number_input("House Value (£)", min_value=50000, max_value=2000000,
                                                      value=entry['house_value'], key=f"house_value_{i}")
                updated_month_acquisition = st.number_input("Month of Acquisition", min_value=1,
                                                            value=entry['month_acquisition'], key=f"month_acquisition_{i}")
                updated_appreciation_rate = st.number_input("Yearly Property Appreciation (%)", min_value=0.0,
                                                            max_value=20.0, value=entry['appreciation_rate'], step=0.1,
                                                            key=f"appreciation_rate_{i}")
                updated_sale = st.checkbox("Sale", value=entry["sale"], key=f"sale_{i}")
                updated_month_sale = entry["month_sale"]
                if updated_sale:
                    updated_month_sale = st.number_input("Month of Sale", min_value=updated_month_acquisition + 1,
                                                         value=entry["month_sale"] if entry[
                                                             "month_sale"] else updated_month_acquisition + 12,
                                                         key=f"month_sale_{i}")

                updated_mortgage = st.checkbox("Mortgage", value=entry.get("mortgage", False), key=f"mortgage_{i}")
                if updated_mortgage:
                    updated_deposit = st.number_input("Deposit (£)", min_value=0, max_value=updated_house_value,
                                                      value=entry.get("deposit", 0), key=f"deposit_{i}")
                    updated_mortgage_term = st.number_input("Mortgage Term (Years)", min_value=1, max_value=40,
                                                            value=entry.get("mortgage_term", 25), key=f"mortgage_term_{i}")
                    updated_standard_rate = st.number_input("Standard Variable Rate (%)", min_value=0.0, max_value=10.0,
                                                            value=entry.get("standard_rate", 4.0), step=0.1,
                                                            key=f"standard_rate_{i}")

                    if st.button(f"Save Changes for {entry['house_name']}"):
                        df_builder.financial_entry.housing_entries[i] = {
                            "house_name": updated_house_name,
                            "house_value": updated_house_value,
                            "month_acquisition": updated_month_acquisition,
                            "appreciation_rate": updated_appreciation_rate,
                            "sale": updated_sale,
                            "month_sale": updated_month_sale,
                            "mortgage": updated_mortgage,
                            "deposit": updated_deposit if updated_mortgage else 0,
                            "mortgage_term": updated_mortgage_term if updated_mortgage else 0,
                            "standard_rate": updated_standard_rate if updated_mortgage else 0
                        }
                        st.session_state.df = df_builder.rebuild_dataframe()
                        st.success(f"Updated data for {updated_house_name}.")

                    if st.button(f"Delete {entry['house_name']}"):
                        df_builder.financial_entry.housing_entries.pop(i)
                        st.session_state.df = df_builder.rebuild_dataframe()
                        st.success(f"Deleted {entry['house_name']}.")
                        break
