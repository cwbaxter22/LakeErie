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

dirname = os.path.dirname(__file__) #Show cwd, should be ~\FrontEnd
testData = os.path.join(dirname, 'Merged_1127.csv') # CSV needs to have this name
                                                # CSV will eventually be replaced by
                                                # API dataframe

df = pd.read_csv(testData)
df['Time'] = pd.to_datetime(df['Time'])
st.set_page_config(layout="wide") # Page configuration must be first Streamlit command called
st.title("Historical Buoy Data") # Page title

LOCATIONS = list(df['Location'].unique()) # List of all weather station locations
VARIABLES = list(df['variable'].unique()) # List of all variable types

with st.sidebar: # sidebar hides the drop-down
    st.subheader("Configure data selection")
    START_DATE = st.date_input("Choose start-date", min_value=datetime.date(2021, 7, 21), max_value=datetime.date(2023, 8, 1), value = None)
    END_DATE = st.date_input("Choose end-date", value = None)

    LOCATION = st.selectbox(label = "Choose a location", options = LOCATIONS)
    #Figure out how to make this multiselect work
    #LOCATION = st.multiselect('Choose desired locations', LOCATIONS)
    VARIABLE = st.selectbox(label = "Choose a variable", options = VARIABLES)

#Create temporary dataframe based on date range
mask = (df['Time'] > np.datetime64(START_DATE)) & (df['Time'] <= np.datetime64(END_DATE))
df_intime = df.loc[mask]

# Configure temporary dataframe to queried values
df_viz = df_intime.query(f"Location=='{LOCATION}'").query(f"variable=='{VARIABLE}'")

# Title of plot
GRAPH_TITLE = f"{VARIABLE} over Time for {LOCATION}"
#Create plot figure
fig = px.scatter(df_viz, x = "Time", y = "value", title = GRAPH_TITLE, color = "Location", labels={"value": f"{VARIABLE}"})
# Plot creation
st.plotly_chart(fig)

#Display dataframe of plotted data
st.dataframe(df_viz)
