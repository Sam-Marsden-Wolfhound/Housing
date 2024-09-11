import streamlit as st
import plotly.express as px
import matplotlib.pyplot as plt


def display_graph(title, dataframe, default_columns=[]):
    with st.container(border=True):
        st.subheader(title)
        if not dataframe.empty:

            df = dataframe.copy()

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





def display_graph_plotly(title, dataframe, default_columns=[]):
    with st.container():
        st.subheader(title)
        if not dataframe.empty:
            df = dataframe.copy()

            min_index = 0
            max_index = len(df) - 1

            # Create sliders to select the start and end times
            start = st.slider(
                'Select start time',
                min_value=min_index,
                max_value=max_index,
                value=min_index,
                key=f'{title}_min'
            )
            end = st.slider(
                'Select end time',
                min_value=min_index,
                max_value=max_index,
                value=min(max_index, 300),  # Limit default to 300 if max_index is larger
                key=f'{title}_max'
            )

            # Ensure that the end time is after the start time
            if start > end:
                st.error('End time must be after start time')
                return

            # Filter the DataFrame based on the selected start and end times
            df_filtered = df.iloc[start:end+1]

            # Let the user select columns to plot
            columns_to_plot = st.multiselect(
                "Select columns to plot",
                df_filtered.columns.tolist(),
                default=default_columns
            )

            if columns_to_plot:
                # Use Plotly to create the graph with a specified x-axis column
                fig = px.line(
                    df_filtered,
                    x='Year-Month',
                    y=columns_to_plot,
                    labels={'x': 'Year-Month'}
                )

                # Reduce the number of x-axis labels displayed by controlling the number of ticks (nticks)
                fig.update_xaxes(
                    type='category',
                    nticks=25,  # Adjust the number of x-axis ticks (fewer labels)
                    tickangle=45,  # Rotate labels by 45 degrees
                    tickmode='auto',
                    tickfont=dict(size=14),  # Adjust font size for better readability
                )

                # Increase space between x-axis labels by padding
                # fig.update_layout(
                #     xaxis_tickformat='%Y-%m',
                #     margin=dict(l=40, r=40, t=40, b=120)  # Add padding to the bottom for label space
                # )

                st.plotly_chart(fig)


