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
                value=300,
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

