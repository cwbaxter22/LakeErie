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


dirname = os.path.dirname(__file__) #Relative path to /pages
st.set_page_config(layout="wide") # Page configuration must be first Streamlit command called
st.title("Historical Buoy Data") # Page title

#Hourly or daily choice - default is daily
frequency_selected = st.radio(
    "Select data interval",
    ["Hourly", "Daily"],
    index=1
)

if frequency_selected == "Daily":
    df = df_creation(dirname, "/daily_tidy_all_data.csv")
else:
    df = df_creation(dirname, "/hourly_tidy_all_data.csv")

if df.empty:
    st.write(":red[Please select a data collection site from the drop-down above]" )
else:
    #Convert time column to datetime
    df['times'] = pd.to_datetime(df['times'])
    locations_in_df = list(df['location'].unique()) # List of all weather station locations
    variables_in_df = list(df['parameter'].unique()) # List of all variable types
    with st.sidebar: # sidebar hides the drop-down
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
        VARIABLE = st.selectbox(label = "Choose a variable",
                                options = variables_in_df,
                                index=0)
    try:
        #Create temporary dataframe based on date range
        mask = (df['times'] > np.datetime64(START_DATE)) & (df['times'] <= np.datetime64(END_DATE))
        df_intime = df.loc[mask]
        # Configure temporary dataframe to queried values
        df_viz = df_intime.query(
            "location == @locations_to_graph").query(
                f"parameter=='{VARIABLE}'")
        # Title of plot
        GRAPH_TITLE = f"{VARIABLE} over Time for {locations_to_graph}"
        #Create plot figure
        fig = px.scatter(df_viz, x = "times",
                         y = "value_mean",
                         title = GRAPH_TITLE,
                         color = "location",
                         error_y = "value_std",
                         labels={"value_mean": f"{VARIABLE} [{df_viz['Units'][0]}]",
                                 "times" : "Time"})
        # Plot creation
        st.plotly_chart(fig)
        #Display dataframe of plotted data
        st.write("Data from graph above")
        st.dataframe(df_viz, column_order=['location',
                                           'parameter',
                                           'value_mean',
                                           'Units',
                                           'value_std',
                                           'times'])
    except KeyError:
        st.write(":red[Please fill in all configuration settings]")
