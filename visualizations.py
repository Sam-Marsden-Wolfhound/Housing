import streamlit as st
import matplotlib.pyplot as plt


def display_graph(title, dataframe, default_columns=[]):
    with st.container(border=True):
        st.subheader(title)
        if not dataframe.empty:

            df = dataframe

            min_index = df.index.min()
            max_index = df.index.max()

            # Create sliders to select the start and end times
            start = st.slider(
                'Select start time',
                min_value=int(min_index),
                max_value=int(max_index),
                value=int(min_index),
                key=f'{title}_min'
            )
            end = st.slider(
                'Select end time',
                min_value=int(min_index),
                max_value=int(max_index),
                value=int(max_index),
                key=f'{title}_max'
            )

            # Ensure that the end time is after the start time
            if start > end:
                st.error('End time must be after start time')
                return

            # Filter the DataFrame based on the selected start and end times
            df_filtered = df.loc[start:end]

            columns_to_plot = st.multiselect("Select columns to plot",
                                             df_filtered.columns.tolist(),
                                             default=default_columns
            )
            if columns_to_plot:
                st.line_chart(df_filtered[columns_to_plot])


def display_salary_graph():
    st.subheader("Salary Graph")
    if not st.session_state.combined_salary_df.empty:

        df = st.session_state.combined_salary_df

        min_index = df.index.min()
        max_index = df.index.max()

        # Create sliders to select the start and end times
        start = st.slider("Select start time", min_value=int(min_index), max_value=int(max_index), value=int(min_index), key="sal_min")
        end = st.slider("Select end time", min_value=int(min_index), max_value=int(max_index), value=int(max_index), key="sal_max")

        # Ensure that the end time is after the start time
        if start > end:
            st.error("End time must be after start time")
            return

        # Filter the DataFrame based on the selected start and end times
        df_filtered = df.loc[start:end]

        columns_to_plot = st.multiselect("Select columns to plot",
                                         df_filtered.columns.tolist(),
                                         default=["Monthly Salary",
                                                  "Take Home Pay"]
        )
        if columns_to_plot:
            st.line_chart(df_filtered[columns_to_plot])


def display_expenses_graph():
    st.subheader("Expenses Graph")
    if not st.session_state.combined_expenses_df.empty:
        df = st.session_state.combined_expenses_df

        min_index = df.index.min()
        max_index = df.index.max()

        # Create sliders to select the start and end times
        start = st.slider("Select start time", min_value=int(min_index), max_value=int(max_index), value=int(min_index), key="exp_min")
        end = st.slider("Select end time", min_value=int(min_index), max_value=int(max_index), value=int(max_index), key="exp_max")

        # Ensure that the end time is after the start time
        if start > end:
            st.error("End time must be after start time")
            return

        # Filter the DataFrame based on the selected start and end times
        df_filtered = df.loc[start:end]

        columns_to_plot = st.multiselect("Select columns to plot",
                                         df_filtered.columns.tolist(),
                                         default=["Monthly Expenses"]
                                         )
        if columns_to_plot:
            st.line_chart(df_filtered[columns_to_plot])

def display_housing_and_rent_graph():
    st.subheader("Housing & Rent Graph")
    if not st.session_state.combined_housing_and_rent_df.empty:
        df = st.session_state.combined_housing_and_rent_df

        min_index = df.index.min()
        max_index = df.index.max()

        # Create sliders to select the start and end times
        start = st.slider("Select start time", min_value=int(min_index), max_value=int(max_index), value=int(min_index), key="hous_min")
        end = st.slider("Select end time", min_value=int(min_index), max_value=int(max_index), value=int(max_index), key="hous_max")

        # Ensure that the end time is after the start time
        if start > end:
            st.error("End time must be after start time")
            return

        # Filter the DataFrame based on the selected start and end times
        df_filtered = df.loc[start:end]

        columns_to_plot = st.multiselect("Select columns to plot",
                                         df_filtered.columns.tolist(),
                                         default=["Row Total Payment Amount",
                                                  "Row Total Interest Amount",
                                                  "Row Total Rent Amount"]
                                         )
        if columns_to_plot:
            st.line_chart(df_filtered[columns_to_plot])



def display_stock_graph():
    st.subheader("Stock Graph")
    if not st.session_state.combined_stock_df.empty:
        df = st.session_state.combined_stock_df

        min_index = df.index.min()
        max_index = df.index.max()

        # Create sliders to select the start and end times
        start = st.slider("Select start time", min_value=int(min_index), max_value=int(max_index), value=int(min_index), key="stock_min")
        end = st.slider("Select end time", min_value=int(min_index), max_value=int(max_index), value=int(max_index), key="stock_max")

        # Ensure that the end time is after the start time
        if start > end:
            st.error("End time must be after start time")
            return

        # Filter the DataFrame based on the selected start and end times
        df_filtered = df.loc[start:end]

        columns_to_plot = st.multiselect("Select columns to plot",
                                         df_filtered.columns.tolist(),
                                         default=["Running Total Investment Amount",
                                                  "Running Total Cash Value",
                                                  "Running Total Cashout Amount Stocks",
                                                  "Delta"]
                                         )
        if columns_to_plot:
            st.line_chart(df_filtered[columns_to_plot])

def display_savings_graph():
    st.subheader("Savings Graph")
    if not st.session_state.combined_savings_df.empty:
        df = st.session_state.combined_savings_df

        min_index = df.index.min()
        max_index = df.index.max()

        # Create sliders to select the start and end times
        start = st.slider("Select start time", min_value=int(min_index), max_value=int(max_index), value=int(min_index), key="save_min")
        end = st.slider("Select end time", min_value=int(min_index), max_value=int(max_index), value=int(max_index), key="save_max")

        # Ensure that the end time is after the start time
        if start > end:
            st.error("End time must be after start time")
            return

        # Filter the DataFrame based on the selected start and end times
        df_filtered = df.loc[start:end]

        columns_to_plot = st.multiselect("Select columns to plot",
                                         df_filtered.columns.tolist(),
                                         default=["Row Total Asset Value"]
                                         )
        if columns_to_plot:
            st.line_chart(df_filtered[columns_to_plot])

def display_analysis_graph():
    st.subheader("Analysis Graph")
    if not st.session_state.combined_analysis_df.empty:
        """
        Display an analysis graph with start and end times for the x-axis set by the user.
    
        :param df: The combined DataFrame to plot.
        """
        # Get the minimum and maximum indices from the DataFrame for the slider
        min_index = st.session_state.combined_analysis_df.index.min()
        max_index = st.session_state.combined_analysis_df.index.max()

        # Create sliders to select the start and end times
        start = st.slider("Select start time", min_value=int(min_index), max_value=int(max_index), value=int(min_index), key="anal_min")
        end = st.slider("Select end time", min_value=int(min_index), max_value=int(max_index), value=int(max_index), key="anal_max")

        # Ensure that the end time is after the start time
        if start > end:
            st.error("End time must be after start time")
            return

        # Filter the DataFrame based on the selected start and end times
        df_filtered = st.session_state.combined_analysis_df.loc[start:end]

        columns_to_plot = st.multiselect("Select columns to plot",
                                         df_filtered.columns.tolist(),
                                         default=[])
        if columns_to_plot:
            st.line_chart(df_filtered[columns_to_plot])

