"""Manipulate and plot data from dataframes.

Module contains 4 functions: 1 for dataframe manipulation, 3 for plotting.
Dataframe manipulation is all encompassing should not need to be used with
any other manipulation tools. Two of the plotting functions generate different figures,
while the third is able to plot any scatter plot figure.

"""

# Notice the blank line above. Code should continue on this line."""

import datetime
import streamlit as st
import pandas as pd
import plotly.express as px
from plotly import graph_objects
import numpy as np

def df_creation(path_to_df: str) -> [pd.DataFrame(), str, list, str, str]:
    """
    Create dataframe using user-selected sites.

    Arguments:
    ----------
    path_to_df (str): path to ../data/processed/combined/ folder within github
    
    Returns:
    ----------
    df_loc_time_selection (df): df containing user selected variables at chosen locations and times
    variable_to_plot (str): scalar variable to be plotted against time
    locations_to_graph (list): list of locations that are contained in the df
    start_time (datetime): starting date and hour or just starting date \
          (depending on frequency selection) of data collection. 
    end_time (datetime): end date and hour or just end date \
          (depending on frequency selection) of data collection.

    """

    frequency_selected = st.radio(
        "Select data interval",
        ["Hourly", "Daily"],
        index=1
    )
    # Set location to correct frequency csv
    if frequency_selected == "Daily":
        data_frequency = "/daily_data.csv"
    else:
        data_frequency = "/hourly_data.csv"
    #Hourly or daily choice - default is daily
    st.subheader("Select data locations")
    # Static list of data collection sites
    # Names of the csv files
    sites_csv_name = ["Beach2_Buoy",
                             "Beach2_Tower",
                             "Beach6_Buoy",
                             "Near_Shore_Buoy",
                             "Surface_Data",
                             "Walnut_Creek",
                             "Trec_Tower"]
    # Names of locations user can pick from
    sites_display_name = ["Beach 2 Buoy",
                         "Beach 2 Tower",
                         "Beach 6 Buoy",
                         "Near Shore Buoy",
                         "Surface Data",
                         "Walnut Creek",
                         "TREC Tower"]
    # Checkboxes for user to select collection sites
    locations_selected_display = st.multiselect(
        "Data collection sites",
        sites_display_name,
        default=sites_display_name[-1],
    )
    # Create a new list of 1's and 0's
    # 1's index the desired location of the formatted location string
    # in sites_display_name
    indices = [x in locations_selected_display for x in sites_display_name]
    # Index the array containing all  of the available csv names using
    # the previously generated index array such that the correct csv names are
    # selected.
    locations_selected_call = np.asarray(sites_csv_name)[np.asarray(indices).astype(bool)]
    # If the user has not chosen any locations,
    # return a blank df
    if len(locations_selected_call) == 0:
        df_chosen_locs = pd.DataFrame()
        return df_chosen_locs
    else:
        # List comprehension to create list of paths to needed dataframes
        df_dirs = [(path_to_df + loc
                        + data_frequency) for loc in locations_selected_call]
        # Concatenate all of the dfs into one
        df_chosen_locs = pd.concat(map(pd.read_csv, df_dirs))
        # When user has not made a selection, display error message
    if df_chosen_locs.empty:
        st.write(":red[Please select a data collection site from the drop-down above]" )
    else:
        #Convert time column to datetime
        df_chosen_locs['times'] = pd.to_datetime(df_chosen_locs['times'])
        # List of all weather station locations
        locations_in_df = list(df_chosen_locs['location'].unique())
        # List of all variable types
        variables_in_df = list(df_chosen_locs['parameter'].unique())
        # Sidebar hides the drop-down
        with st.sidebar:
            st.subheader("Configure data selection")
            start_time = st.date_input("Choose start-date",
                                    min_value=datetime.date(2000, 1, 1),
                                    max_value=datetime.date(2023, 9, 1),
                                    value = datetime.date(2000, 1, 1))
            end_time = st.date_input("Choose end-date",
                                    value = datetime.date(2023, 9, 1))
            locations_to_graph = st.multiselect('Choose desired locations',
                                                locations_in_df,
                                                default=locations_in_df[0])
            variable_to_plot = st.selectbox(label = "Choose a variable",
                                    options = variables_in_df,
                                    index=0)
            # Create temporary dataframe based on date range
            # The mask creates a boolean vector to include only values within date range
            time_mask = (df_chosen_locs['times'] > np.datetime64(start_time)) & \
                        (df_chosen_locs['times'] <= np.datetime64(end_time))
            df_intime = df_chosen_locs.loc[time_mask]
            # Configure visualization dataframe (df_viz) to queried values
            df_loc_time_selection = df_intime.query(
                "location == @locations_to_graph").query(
                    f"parameter=='{variable_to_plot}'")
            return df_loc_time_selection, variable_to_plot, locations_to_graph, start_time, end_time

def create_all_time_fig(df_alltime: pd.DataFrame(),
                        graph_title: str,
                        alltime_var: str,
                        error_bars: bool,
                        locations_to_graph: str,
                        start_date: str,
                        end_date: str) -> graph_objects.Figure():
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
    mask = (df_alltime['times'] > np.datetime64(start_date)) & \
           (df_alltime['times'] <= np.datetime64(end_date))
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
                            hover_data=['Units'],
                            labels={"value_mean": f"{alltime_var}]",
                                    "times" : "Time"})
        #If we want to get units immediately after the label: [{df_figure_data['Units'][9703]}]
        #We would need a row number within the selected data
        #May be a better option another way
    else:
        print(df_figure_data.head())
        all_time_fig = px.scatter(df_figure_data,
                                  x = "times",
                                  y = "value_mean",
                                  title = graph_title,
                                  color = "location",
                                  hover_data=['Units'],
                                  labels={"value_mean": f"{alltime_var}" })
    return all_time_fig

def create_annual_comparison_fig(df_annual:pd.DataFrame(),
                                graph_title: str,
                                comparison_variable:str,
                                error_bars:bool,
                                locations_to_graph:str) -> graph_objects.Figure():
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
                                        f"{comparison_variable}",
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
                                f"{comparison_variable}",
                                "timepoint" : "Month/Day",
                                "location" : "Location",
                                "value_std" : "Std Deviation"
                                })
    return annual_fig

def plot_it(fig_to_plot:graph_objects.Figure, df_viz) -> None:
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
