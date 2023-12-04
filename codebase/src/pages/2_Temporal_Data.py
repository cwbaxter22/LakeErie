"""Module that generates web interface for user to generate plots and view data

This page creates a plot from sites chosen by the user.

Current time comparison setup for setting date range is comparing the time from the
initial dataframe (imported as a string and converted to np64 datetime) to the 
time set from the widget (st.dateinput()) that is initially in datetime.date() and
is then converted to np64 datetime"""

import os
import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objects
import numpy as np

def df_creation(current_file_dir: str,
                 frequency: str) -> pd.DataFrame():
    """
    Create dataframe using user-selected sites.

    Arguments:
    ----------
    current_file_dir (str): current file directory
    frequency (str): frequency of data

    Returns:
    ----------
    df_chosen_locs (df): df containing user selected sites

    """
    st.subheader("Select data locations")
    # Static list of data collection sites
    # Names of the csv files
    LOCATIONS_UNFORMATTED = ["Beach2_Buoy", "Beach2_Tower", "Beach6_Buoy", "TREC_Tower"]
    # Names of locations user can pick from
    LOCATIONS_DISPLAY = ["Beach 2 Buoy", "Beach 2 Tower", "Beach 6 Buoy", "TREC Tower"]
    # Checkboxes for user to select collection sites
    locations_selected_display = st.multiselect(
        "Data collection sites",
        LOCATIONS_DISPLAY,
        default=LOCATIONS_DISPLAY[-1],
    )
    # Create a new list of 1's and 0's
    # 1's index the desired location of the formatted location string
    # in LOCATIONS_DISPLAY
    indices = [x in locations_selected_display for x in LOCATIONS_DISPLAY]
    # Index the array containing all  of the available csv names using
    # the previously generated index array such that the correct csv names are
    # selected.
    locations_selected_call = np.asarray(LOCATIONS_UNFORMATTED)[np.asarray(indices).astype(bool)]

    # If the user has not chosen any locations,
    # return a blank df
    if len(locations_selected_call) == 0:
        df_chosen_locs = pd.DataFrame()
        return df_chosen_locs
    else:
        # List comprehension to create list of paths to needed dataframes
        df_dirs = [(current_file_dir + "/data/iChart6_data/processed/" + loc
                        + frequency) for loc in locations_selected_call]
        # Concatenate all of the dfs into one
        df_chosen_locs = pd.concat(map(pd.read_csv, df_dirs))
        return df_chosen_locs

def create_all_time_fig(df_alltime: pd.DataFrame(),
                        graph_title: str,
                        alltime_var: str,
                        error_bars: bool) -> graph_objects.Figure():
    """
    Create chronological figure based on date range user inputs.

    Arguments:
    ----------
    df_alltime (pd.DataFrame): df containing variables within selected date range
    graph_title (str): Title for the figure
    alltime_var (str): Variable that will be evaluated
    error_bars (bool): Boolean indicating whether or not error bars will be applied in the figure

    Returns:
    ----------
    all_time_fig (graph_objects.Figure): Final formatted figure for the chronological data

    """
    # Title of plot
    graph_title = f"{alltime_var} over Time for {locations_to_graph}"
    mask = (df_alltime['times'] > np.datetime64(START_DATE)) & \
           (df_alltime['times'] <= np.datetime64(END_DATE))
    df_inrange = df_alltime.loc[mask]
    # Configure temporary dataframe to queried values
    df_figure_data = df_inrange.query(
        "location == @locations_to_graph").query(
            f"parameter=='{alltime_var}'")
    # Title of plot
    graph_title = f"{alltime_var} over Time for {locations_to_graph}"
    # Create plot figure
    # Only difference in the if/else is if error bars are applied
    if error_bars:
        all_time_fig = px.scatter(df_figure_data, x = "times",
                            y = "value_mean",
                            title = graph_title,
                            color = "location",
                            error_y = "value_std",
                            labels={"value_mean": f"{alltime_var} [{df_figure_data['Units'][0]}]",
                                    "times" : "Time"})
    else:
        all_time_fig = px.scatter(df_figure_data, x = "times",
                        y = "value_mean",
                        title = graph_title,
                        color = "location",
                        labels={"value_mean": f"{alltime_var} [{df_figure_data['Units'][0]}]",
                                "times" : "Time"})
    return all_time_fig

def create_annual_comparison_fig(df_annual:pd.DataFrame(),
                                graph_title: str,
                                comparison_variable:str,
                                error_bars:bool) -> graph_objects.Figure():
    """
    Create annual comparison figure based on date range and years user inputs.

    Arguments:
    ----------
    df_annual (pd.DataFrame): df containing variables within selected date range
    graph_title (str): Title for the figure
    comparison_var (str): Variable that will be evaluated
    error_bars (bool): Boolean indicating whether or not error bars will be applied in the figure

    Returns:
    ----------
    annual_fig (graph_objects.Figure): Final formatted figure for annual comparisons

    """
    # Confirm time column is in pd datetime timestamp format
    df_annual['times'] = pd.to_datetime(df_annual['times'])
    # Sort out the years into separate column
    # Clearly DateTime does have a year, month, and day member, so these warnings are disabled below
    df_annual['year'] = pd.DatetimeIndex(df_annual['times']).year.astype(str) # pylint: disable=E1101
    # Determine what years dataset encompasses
    unique_years = df_annual['year'].unique()
    # Prompt user for years to have in graph comparison
    comparison_years = st.multiselect(
    'Choose years to compare',
    unique_years
    )
    # Filter df to only contain comparison variable
    var_mask = df_annual['parameter']==comparison_variable
    df_spec_var = df_annual.loc[var_mask]
    # Filter df to only contain dates chosen from previous user prompt
    df_yearly_comp = df_spec_var[df_spec_var['year'].isin(comparison_years)]
    df_yearly_comp['month'] = pd.DatetimeIndex(df_yearly_comp['times']).month # pylint: disable=E1101
    df_yearly_comp['day'] = pd.DatetimeIndex(df_yearly_comp['times']).day # pylint: disable=E1101
    try:
        df_yearly_comp['hour'] = df_yearly_comp['times'].datetime.hour
        df_yearly_comp['timepoint'] = df_yearly_comp['month'].astype(str) + '/' \
                                    + df_yearly_comp['day'].astype(str) + " " \
                                    + df_yearly_comp['hour']
    # Since the goal is to capture all exceptions, this warning is disabled.
    except: # pylint: disable=bare-except
        df_yearly_comp['timepoint'] = df_yearly_comp['month'].astype(str) + '/' \
                                    + df_yearly_comp['day'].astype(str)
    graph_title = f"{comparison_variable} annual data for {locations_to_graph}"
    if error_bars:
        annual_fig = px.scatter(df_yearly_comp, x = "timepoint",
                                y = "value_mean",
                                title = graph_title,
                                color = "year",
                                symbol = "year",
                                hover_data = ["year", "timepoint", "location", "value_std"],
                                error_y = "value_std",
                                labels={"value_mean": \
                                        f"{comparison_variable} [{df_yearly_comp['Units'][0]}]",
                                        "timepoint" : "Month/Day",
                                        "location" : "Location",
                                        "value_std" : "Std Deviation"
                                        })
    else:
        annual_fig = px.scatter(df_yearly_comp, x = "timepoint",
                        y = "value_mean",
                        title = graph_title,
                        color = "year",
                        symbol = "year",
                        hover_data = ["year", "timepoint", "location", "value_std"],
                        labels={"value_mean": \
                                f"{comparison_variable} [{df_yearly_comp['Units'][0]}]",
                                "timepoint" : "Month/Day",
                                "location" : "Location",
                                "value_std" : "Std Deviation"
                                })
    return annual_fig

def plot_it(fig_to_plot:graph_objects.Figure) -> None:
    """
    Plot figure based on preset characteristics. Provide features to adjust figure representation.

    Arguments:
    ----------
    fig_to_plot (px.graph_objs.Figure): Plotly figure to be plotted

    Returns:
    ----------
    None

    """
    # Generate sliders for users to adjust graph dimensions
    # Default graph size is 900px x 900px
    px_width = st.slider('Plot width', value = 900, min_value=500, max_value=2000, step=25)
    px_height = st.slider('Plot height', value = 900, min_value=500, max_value=2000, step=25)
    fig_to_plot.update_traces(marker_size=5)
    fig_to_plot.update_layout(scattermode="group", scattergap=0.9)
    fig_to_plot.update_layout(
    autosize=False,
    width=px_width,
    height=px_height,
    )
    # Plot creation
    st.plotly_chart(fig_to_plot)
    # Display dataframe of plotted data
    st.header("Tabulated data for graph above")
    st.dataframe(df_viz, column_order=['location',
                                        'parameter',
                                        'value_mean',
                                        'Units',
                                        'value_std',
                                        'times'])

# Initial Streamlit page setup
# Page configuration must be first Streamlit command called
st.set_page_config(layout="wide")
st.title("Historical Buoy Data")

#Hourly or daily choice - default is daily
frequency_selected = st.radio(
    "Select data interval",
    ["Hourly", "Daily"],
    index=1
)

# Relative path to /pages
dirname = os.path.dirname(__file__)
# Set location to correct frequency csv
if frequency_selected == "Daily":
    df = df_creation(dirname, "/daily_tidy_all_data.csv")
else:
    df = df_creation(dirname, "/hourly_tidy_all_data.csv")

# When user has not made a selection, display error message
if df.empty:
    st.write(":red[Please select a data collection site from the drop-down above]" )
else:
    #Convert time column to datetime
    df['times'] = pd.to_datetime(df['times'])
    # List of all weather station locations
    locations_in_df = list(df['location'].unique())
    # List of all variable types
    variables_in_df = list(df['parameter'].unique())
    # Sidebar hides the drop-down
    with st.sidebar:
        st.subheader("Configure data selection")
        START_DATE = st.date_input("Choose start-date",
                                   min_value=datetime.date(2000, 1, 1),
                                   max_value=datetime.date(2023, 9, 1),
                                   value = datetime.date(2000, 1, 1))
        END_DATE = st.date_input("Choose end-date",
                                 value = datetime.date(2023, 9, 1))
        locations_to_graph = st.multiselect('Choose desired locations',
                                            locations_in_df,
                                            default=locations_in_df[0])
        variable_to_plot = st.selectbox(label = "Choose a variable",
                                options = variables_in_df,
                                index=0)
        # Create temporary dataframe based on date range
        # The mask creates a boolean vector to include only values within date range
        time_mask = (df['times'] > np.datetime64(START_DATE)) & \
                    (df['times'] <= np.datetime64(END_DATE))
        df_intime = df.loc[time_mask]
        # Configure visualization dataframe (df_viz) to queried values
        df_viz = df_intime.query(
            "location == @locations_to_graph").query(
                f"parameter=='{variable_to_plot}'")
    try:
        # Choose between either chronological or annual comparison view
        data_comparison_type = st.radio(
        "Choose graph type",
        ["Chronological",
         "Annual Comparison"],
        captions = ["View chronology of chosen variable at one or more locations from "
                    "selected start to end date",
                    "Compare annual trends for one variable at one location."])
        error_bars_on = st.toggle("Display error bars")
        if data_comparison_type == "Chronological":
            fig = create_all_time_fig(df_viz,
                                      "Chronological Timeline",
                                      variable_to_plot,
                                      error_bars_on)
            plot_it(fig)
        else:
            # Generate annual data overlap
            an_fig = create_annual_comparison_fig(df_viz,
                                    "Annual Data Comparison",
                                    variable_to_plot,
                                    error_bars_on)
            plot_it(an_fig)
    # Since the goal is to capture all exceptions, this warning is disabled.
    except: # pylint: disable=bare-except
        st.write(":red[Please fill in all configuration settings]")
