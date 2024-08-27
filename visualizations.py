import streamlit as st

def display_salary_graph():
    st.subheader("Salary Graph")
    if not st.session_state.combined_salary_df.empty:
        columns_to_plot = st.multiselect("Select columns to plot", st.session_state.combined_salary_df.columns.tolist(), default=["Monthly Salary"])
        if columns_to_plot:
            st.line_chart(st.session_state.combined_salary_df[columns_to_plot])

def display_expenses_graph():
    st.subheader("Expenses Graph")
    if not st.session_state.combined_expenses_df.empty:
        columns_to_plot = st.multiselect("Select columns to plot", st.session_state.combined_expenses_df.columns.tolist(), default=["Monthly Expenses"])
        if columns_to_plot:
            st.line_chart(st.session_state.combined_expenses_df[columns_to_plot])

def display_housing_graph():
    st.subheader("Housing Graph")
    if not st.session_state.combined_housing_df.empty:
        columns_to_plot = st.multiselect("Select columns to plot", st.session_state.combined_housing_df.columns.tolist())
        if columns_to_plot:
            st.line_chart(st.session_state.combined_housing_df[columns_to_plot])


