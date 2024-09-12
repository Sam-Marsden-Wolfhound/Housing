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
    with st.container(border=True):
        st.subheader(title)
        if not dataframe.empty:
            df = dataframe.copy()

            min_index = 0
            max_index = len(df) - 1

            # Let the user select columns to plot
            columns_to_plot = st.multiselect(
                "Select columns to plot",
                df.columns.tolist(),
                default=default_columns
            )

            if columns_to_plot:
                with st.expander("X & Y Axis", expanded=False):
                    st.subheader("X-axis", divider=False)
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
                        value=min(max_index, 400),  # Limit default to 300 if max_index is larger
                        key=f'{title}_max'
                    )

                    # Ensure that the end time is after the start time
                    if start > end:
                        st.error('End time must be after start time')
                        return

                    # Filter the DataFrame based on the selected start and end times
                    df_filtered = df.iloc[start:end + 1]

                    st.subheader("Y-axis", divider=False)
                    # Get the min and max values in the selected columns to define y-axis limits
                    min_value = df_filtered[columns_to_plot].min().min()
                    max_value = df_filtered[columns_to_plot].max().max()

                    # Use Plotly to create the graph with a specified x-axis column
                    fig = px.line(
                        df_filtered,
                        x='Year-Month',
                        y=columns_to_plot,
                        labels={'x': 'Year-Month'}
                    )

                    if not min_value == max_value:
                        # Add sliders to allow users to limit the y-axis range
                        y_min = st.slider(
                            "Select lower bound of y-axis",
                            min_value=float(min_value),
                            max_value=0.01,
                            value=float(min_value),
                            step=(0.01 - min_value) / 100,
                            key=f'{title}_y_min'
                        )

                        y_max = st.slider(
                            "Select upper bound of y-axis",
                            min_value=0.01,
                            max_value=float(max_value),
                            value=float(max_value),
                            step=(max_value - 0.01) / 100,
                            key=f'{title}_y_max'
                        )

                        if y_min >= y_max:
                            st.error('Upper bound must be greater than lower bound')
                            return

                        # Set y-axis limits
                        fig.update_yaxes(range=[y_min, y_max])

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


