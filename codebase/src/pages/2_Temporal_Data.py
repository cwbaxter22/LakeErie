"""Module that generates web interface for user to generate plots and view data

Please, please read this line:
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

def df_creation(dir, frequency):
    st.subheader("Select data locations")
    #Static list of data collection sites
    LOCATIONS = ["Beach2_Buoy", "Beach2_Tower", "Beach6_Buoy", "TREC_Tower"]
    # Checkboxes for user to select collection sites
    locations_selected = st.multiselect(
        "Data collection sites",
        LOCATIONS
    )
    # List comprehension to create list of paths to needed dataframes
    df_dirs = [(dir + "/data/iChart6_data/processed/" + loc + frequency) for loc in locations_selected]
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
    index=0
)

if frequency_selected == "Daily":
    df = df_creation(dirname, "/daily_tidy_all_data.csv")
else:
    df = df_creation(dirname, "/hourly_tidy_all_data.csv")

#Convert time column to datetime
df['times'] = pd.to_datetime(df['times'])

locations_in_df = list(df['location'].unique()) # List of all weather station locations
variables_in_df = list(df['parameter'].unique()) # List of all variable types

with st.sidebar: # sidebar hides the drop-down
    st.subheader("Configure data selection")
    START_DATE = st.date_input("Choose start-date", min_value=datetime.date(2008, 1, 1), max_value=datetime.date(2023, 9, 1), value = None)
    END_DATE = st.date_input("Choose end-date", value = None)

    LOCATION = st.selectbox(label = "Choose a location", options = locations_in_df)
    #Figure out how to make this multiselect work
    #LOCATION = st.multiselect('Choose desired locations', LOCATIONS)
    VARIABLE = st.selectbox(label = "Choose a variable", options = variables_in_df)

#Create temporary dataframe based on date range
mask = (df['times'] > np.datetime64(START_DATE)) & (df['times'] <= np.datetime64(END_DATE))
df_intime = df.loc[mask]

# Configure temporary dataframe to queried values
df_viz = df_intime.query(f"location=='{LOCATION}'").query(f"parameter=='{VARIABLE}'")

# Title of plot
GRAPH_TITLE = f"{VARIABLE} over Time for {LOCATION}"
#Create plot figure
fig = px.scatter(df_viz, x = "times", y = "value_mean", title = GRAPH_TITLE, color = "location", labels={"value_mean": f"{VARIABLE}", "times" : "time"})
# Plot creation
st.plotly_chart(fig)

#Display dataframe of plotted data
st.dataframe(df_viz)
