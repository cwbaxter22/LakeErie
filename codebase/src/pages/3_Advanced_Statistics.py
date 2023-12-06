import os
import streamlit as st
import pandas as pd
import numpy as np
import pytimetk
import plotly.io as pio


####### Function to create dataframe #######

def df_creation(current_file_dir: str, frequency: str, selected_location: str) -> pd.DataFrame:
    """
    Create dataframe using user-selected site.

    Arguments:
    ----------
    current_file_dir (str): current file directory
    frequency (str): frequency of data
    selected_location (str): user-selected location

    Returns:
    ----------
    df_chosen_loc (df): df containing user-selected location data
    """
    st.subheader("Select a data location")
    # Static list of data collection sites
    # Names of the csv files
    LOCATIONS_UNFORMATTED = ["Beach2_Buoy", "Beach2_Tower", "Beach6_Buoy", "TREC_Tower"]
    # Names of locations user can pick from
    LOCATIONS_DISPLAY = ["Beach 2 Buoy", "Beach 2 Tower", "Beach 6 Buoy", "TREC Tower"]
    
    # Allow the user to choose one location from the dropdown menu
    selected_location = st.selectbox("Choose a data collection site", LOCATIONS_DISPLAY)
    
    # Index the array containing all of the available csv names using the selected location
    location_index = LOCATIONS_DISPLAY.index(selected_location)
    location_selected_call = LOCATIONS_UNFORMATTED[location_index]

    # List comprehension to create a list of paths to needed dataframes
    df_dir = current_file_dir + "/data/iChart6_data/processed/" + location_selected_call + frequency

    # Read the selected location's dataframe
    df_chosen_loc = pd.read_csv(df_dir)
    return df_chosen_loc


##### Function to create the time series trendline 
def create_trendline(data):
    """
    Use pytimetk to create a non-linear trendline plot for the selected data

    Arguments:
    - data (pandas.DataFrame): The input data containing the 'times' and 'value_mean' columns of one variable.

    Returns:
    - fig (plotly.graph_objects.Figure): Plotly figure object showing the chosen variable over the selected time period, with a non-linear trendline.

    Raises:
    - ValueError: If the 'times' or 'value_mean' column does not exist in the data.
    - ValueError: If the 'times' column is not a datetime object.
    - ValueError: If there is no data in either the 'times' or 'value_mean' column.
    - ValueError: If there is a non-numeric value in the 'value_mean' column.
    """

    fig = pytimetk.plot_timeseries(
        data=data,
        date_column='times',
        value_column='value_mean'
    )
    
    return fig





###########################################################################################
######### Streamlit #######################################################################
########################################################################################### 

st.set_page_config(page_title="Advanced Statistics", layout="wide")
st.title("Advanced Statistics")

file_path = "/Users/benjaminmakhlouf/Downloads/daily_tidy_all_data.csv"
df = pd.read_csv(file_path)

# Relative path to /pages
#dirname = os.path.dirname(__file__)
#df = df_creation(dirname, "/daily_tidy_all_data.csv", selected_location="")

df['times'] = pd.to_datetime(df['times']) #make sure times in the datetime
df['value_mean'] = pd.to_numeric(df['value_mean']) #make sure value_mean is numeric


# Drop down menu for the user to choose the selected frequency, stored in selected_frequency
selected_frequency = st.selectbox("Select data interval", ["Hourly", "Daily"], index=1)
# Drop down menu for the user to chose the selected parameter, stored in selected_parameter 
selected_parameter = st.selectbox("Select Parameter", ["Air_Temperature", "Barometric_Pressure", "Daily_Rain"])

#selected_parameter = "Air_Temperature"
print(df)
#create a new data frame that is the new selected parameter only 
df_param = df[df['parameter'] == selected_parameter]

print(df_param)
#Call the create_trendline function to create the trendline figure 
fig = create_trendline(df_param)

#pio.show(fig)
st.plotly_chart(fig)
