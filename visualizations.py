import streamlit as st

def display_salary_graph():
    st.subheader("Salary Graph")
    if not st.session_state.combined_salary_df.empty:
        columns_to_plot = st.multiselect("Select columns to plot", st.session_state.combined_salary_df.columns.tolist(), default=["Monthly Salary", "Take Home Pay"])
        if columns_to_plot:
            st.line_chart(st.session_state.combined_salary_df[columns_to_plot])

def display_expenses_graph():
    st.subheader("Expenses Graph")
    if not st.session_state.combined_expenses_df.empty:
        columns_to_plot = st.multiselect("Select columns to plot", st.session_state.combined_expenses_df.columns.tolist(), default=["Monthly Expenses"])
        if columns_to_plot:
            st.line_chart(st.session_state.combined_expenses_df[columns_to_plot])

def display_housing_and_rent_graph():
    st.subheader("Housing & Rent Graph")
    if not st.session_state.combined_housing_and_rent_df.empty:
        columns_to_plot = st.multiselect("Select columns to plot", st.session_state.combined_housing_and_rent_df.columns.tolist())
        if columns_to_plot:
            st.line_chart(st.session_state.combined_housing_and_rent_df[columns_to_plot])

def display_stock_graph():
    st.subheader("Stock Graph")
    if not st.session_state.combined_stock_df.empty:
        columns_to_plot = st.multiselect("Select columns to plot", st.session_state.combined_stock_df.columns.tolist(), default=["Running Total Investment Amount", "Running Total Cash Value", "Running Total Cashout Value", "Delta"])
        if columns_to_plot:
            st.line_chart(st.session_state.combined_stock_df[columns_to_plot])

def display_savings_graph():
    st.subheader("Savings Graph")
    if not st.session_state.combined_savings_df.empty:
        columns_to_plot = st.multiselect("Select columns to plot", st.session_state.combined_savings_df.columns.tolist(), default=["Row Total Asset Value"])
        if columns_to_plot:
            st.line_chart(st.session_state.combined_savings_df[columns_to_plot])


def display_analysis_graph():
    pass
