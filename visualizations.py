import streamlit as st
import plotly.express as px
import math


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

def display_graph_overview(title, dataframe, default_columns=[], x1=0, x2=None, y1=0, y2=None, expanded=False):
    with st.expander(f'{title}', expanded=expanded):
        if not dataframe.empty:
            df = dataframe.copy()

            min_index = 0
            max_index = len(df) - 1

            # Let the user select columns to plot
            columns_to_plot = st.multiselect(
                "Select columns to plot",
                df.columns.tolist(),
                default=default_columns,
                key=f'graph_plotly_{title}'
            )

            if columns_to_plot:
                # Filter the DataFrame based on the selected start and end times
                df_filtered = df.iloc[x1:x2]

                # Use Plotly to create the graph with a specified x-axis column
                fig = px.line(
                    df_filtered,
                    x='Year-Month',
                    y=columns_to_plot,
                    labels={'x': 'Year-Month'}
                )

                fig.update_yaxes(range=[y1, y2])

                # Reduce the number of x-axis labels displayed by controlling the number of ticks (nticks)
                fig.update_xaxes(
                    type='category',
                    nticks=25,  # Adjust the number of x-axis ticks (fewer labels)
                    tickangle=45,  # Rotate labels by 45 degrees
                    tickmode='auto',
                    tickfont=dict(size=14),  # Adjust font size for better readability
                )

                # Move the legend below the graph
                fig.update_layout(
                    legend=dict(
                        orientation="h",  # Horizontal legend
                        yanchor="bottom",  # Anchor to the bottom
                        y=-0.5,  # Position below the chart
                        xanchor="center",  # Center horizontally
                        x=0.4  # Center of the x-axis
                    )
                )

                st.plotly_chart(fig)



def display_graph_plotly(title, dataframe, default_columns=[], x1=None, x2=None, y1=None, y2=None):
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
                default=default_columns,
                key=f'graph_plotly_{title}'
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

                        step_value = (max_value) / 100
                        # Find the smallest power of 10 factor that divides step_value
                        step = 10 ** math.floor(math.log10(step_value))

                        y_min = st.slider(
                            "Select lower bound of y-axis",
                            min_value=float(round(min_value, 0)),
                            max_value=0.0,
                            value=float(min_value) if y1 == None else float(y1),
                            step=float(step),
                            key=f'{title}_y_min'
                        )

                        y_max = st.slider(
                            "Select upper bound of y-axis",
                            min_value=0.0,
                            max_value=float(round(max_value, 0)),
                            value=float(max_value) if y2 == None else float(y2),
                            step=float(step),
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

                # Move the legend below the graph
                fig.update_layout(
                    legend=dict(
                        orientation="h",  # Horizontal legend
                        yanchor="bottom",  # Anchor to the bottom
                        y=-0.5,  # Position below the chart
                        xanchor="center",  # Center horizontally
                        x=0.4  # Center of the x-axis
                    )
                )

                st.plotly_chart(fig)


