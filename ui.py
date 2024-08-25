# ui.py

import streamlit as st
import pandas as pd
import plotly.express as px
from dataframe_builder import DataFrameBuilder


class UI:
    def display(self):
        tab1, tab2, tab3, tab4 = st.tabs(["Salary", "Expenses", "Housing", "Analysis"])

        with tab1:
            SalaryUI().display()

        with tab2:
            st.write("Expenses UI - To be implemented")

        with tab3:
            st.write("Housing UI - To be implemented")

        with tab4:
            st.write("Analysis UI - To be implemented")


class SalaryUI:
    def display(self):
        st.header("Salary Inputs")
        self.salary_form()
        self.salary_sidebar()
        self.display_combined_dataframe()
        self.display_salary_plot()

    def salary_form(self):
        with st.form(key="salary_form"):
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                annual_income = st.number_input("Annual Gross Income", min_value=0.0, value=60000.0, step=1000.0)
            with col2:
                pension_pct = st.number_input("Pension Contribution (%)", min_value=0.0, value=3.0, step=0.5)
            with col3:
                company_match_pct = st.number_input("Company Match (%)", min_value=0.0, value=3.0, step=0.5)
            with col4:
                num_months = st.number_input("Number of Months", min_value=1, value=12, step=1)

            entry_name = st.text_input("Entry Name", value=f"Salary {st.session_state.salary_counter}")

            submit = st.form_submit_button("Add Salary Entry")

            if submit:
                st.session_state.salary_entries[entry_name] = {
                    "annual_income": annual_income,
                    "pension_pct": pension_pct,
                    "company_match_pct": company_match_pct,
                    "num_months": num_months
                }
                st.session_state.salary_counter += 1
                st.success(f"Added {entry_name}")

    def salary_sidebar(self):
        st.sidebar.header("Salary Entries")
        entries = st.session_state.salary_entries

        if entries:
            for entry_name, entry_data in entries.items():
                with st.sidebar.expander(entry_name, expanded=False):
                    st.write(f"**Annual Income:** £{entry_data['annual_income']}")
                    st.write(f"**Pension Contribution (%):** {entry_data['pension_pct']}%")
                    st.write(f"**Company Match (%):** {entry_data['company_match_pct']}%")
                    st.write(f"**Number of Months:** {entry_data['num_months']}")

                    edit = st.button(f"Edit {entry_name}", key=f"edit_{entry_name}")
                    delete = st.button(f"Delete {entry_name}", key=f"delete_{entry_name}")

                    if edit:
                        self.edit_salary_entry(entry_name, entry_data)
                    if delete:
                        del st.session_state.salary_entries[entry_name]
                        st.success(f"Deleted {entry_name}")
                        st.experimental_rerun()
        else:
            st.sidebar.info("No salary entries added yet.")

    def edit_salary_entry(self, entry_name, entry_data):
        with st.modal(f"Edit {entry_name}"):
            annual_income = st.number_input("Annual Gross Income", min_value=0.0, value=entry_data['annual_income'],
                                            step=1000.0)
            pension_pct = st.number_input("Pension Contribution (%)", min_value=0.0, value=entry_data['pension_pct'],
                                          step=0.5)
            company_match_pct = st.number_input("Company Match (%)", min_value=0.0,
                                                value=entry_data['company_match_pct'], step=0.5)
            num_months = st.number_input("Number of Months", min_value=1, value=entry_data['num_months'], step=1)

            save = st.button("Save Changes")

            if save:
                st.session_state.salary_entries[entry_name] = {
                    "annual_income": annual_income,
                    "pension_pct": pension_pct,
                    "company_match_pct": company_match_pct,
                    "num_months": num_months
                }
                st.success(f"Updated {entry_name}")
                st.experimental_rerun()

    def display_combined_dataframe(self):
        st.subheader("Combined Salary Data")
        combined_df = DataFrameBuilder.build_salary_dataframe(st.session_state.salary_entries)

        if not combined_df.empty:
            st.dataframe(combined_df)
            st.session_state.combined_salary_df = combined_df
        else:
            st.info("No salary data to display.")

    def display_salary_plot(self):
        if 'combined_salary_df' in st.session_state and not st.session_state.combined_salary_df.empty:
            st.subheader("Salary Data Plot")
            df = st.session_state.combined_salary_df
            columns_to_plot = st.multiselect("Select Columns to Plot", options=df.columns.tolist(),
                                             default=["Gross Income", "Net Income"])

            if columns_to_plot:
                fig = px.line(df, x="Month", y=columns_to_plot, title="Salary Over Time")
                st.plotly_chart(fig)
            else:
                st.warning("Please select at least one column to plot.")
        else:
            st.info("No data available for plotting.")
