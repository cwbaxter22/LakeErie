import os
import streamlit as st
import pandas as pd
import numpy as np
import pytimetk
import plotly.io as pio
import folium
from streamlit_folium import folium_static


#################################
###### FUNCTIONS
# ############################### 


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

### function for anomaly calculation

def create_anomaly_graph(data, period=7, iqr_alpha=0.05, clean_alpha=0.75):
    """
    Use pytimetk to plot a chosen variable over a selected time period, with statistical
    analysis to produce anomaly bars and display values considered as anomalies.

    Arguments:
    - data (pandas.DataFrame): The input data containing the 'times' and 'value_mean' columns.
    - times (datetime): The time column of the data.
    - value_mean (float): The value column of the data.
    - period (int): The period of the data, which is the rolling window for the anomaly detection. 
        Default is 7.
    - iqr_alpha (float): The alpha value for the interquartile range. 
        Smaller IQR values will result in a lower threshold for detecting an anomaly. 
        Default is 0.05.
    - clean_alpha (float): The alpha value for the cleaning. 
        Determines which values should be removed. 
        A smaller clean_alpha will result in more points being completely removed from the dataset. 
        Default is 0.75.

    Returns:
    - anomplot (plotly.graph_objects.Figure): Plotly figure object showing the chosen variable 
        plotted over time, with anomaly bands and points considered as anomalies colored in red.

    Raises:
    - ValueError: If the 'times' or 'value_mean' column does not exist in the data.
    - ValueError: If the 'times' column is not a datetime object.
    - ValueError: If there is no data in either the 'times' or 'value_mean' column.
    - ValueError: If there is a non-numeric value in the 'value_mean' column.
    - ValueError: If the 'period' argument is negative or non-numeric.
    - ValueError: If the 'iqr_alpha' argument is negative or non-numeric.
    - ValueError: If the 'clean_alpha' argument is negative or non-numeric.

    """

    data_cleaned = data.dropna(subset=['value_mean'])

    anomalize_df = pytimetk.anomalize(
        data=data_cleaned,
        date_column='times',
        value_column='value_mean',
        period=period,
        iqr_alpha=iqr_alpha,
        clean_alpha=clean_alpha,
        clean="min_max"
    )

    anomplot = pytimetk.plot_anomalies(
        data=anomalize_df,
        date_column='times',
        engine='plotly',
        title='Plot Anomaly Bands'
    )

    return anomplot


#### Function to create the leaflet map 

def create_leaflet_map(selected_location):
    # Predefined station locations
    stations = {
        "TREQ Station": (42.109657, -80.155201),
        "Bay Bouy": (42.126427, -80.145289),
        "Beach 2 Tower": (42.151768, -80.132625),
        "Beach 2 Bouy": (42.152811, -80.137925),
        "Beach 6 Bouy": (42.157562, -80.131492),
        "Nearshore Bouy": (42.170685, -80.123547),
        "Walnut Creek Bouy": (42.103838, -80.256560),
    }

    latitudes, longitudes = zip(*stations.values())
    map_center = [sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)]

    # Create a Folium map with 'cartodbdark_matter' tile layer
    m = folium.Map(location=map_center, zoom_start=10, tiles='cartodbdark_matter')

    for station, (lat, lon) in stations.items():
        icon_color = 'red' if station == selected_location else 'grey'
        folium.Marker([lat, lon], popup=station, icon=folium.Icon(color=icon_color)).add_to(m)

    return m


### Function for the statistical decomposition 

def anomaly_decomp(data, period=7, iqr_alpha=0.05, clean_alpha=0.75):
    """
    Create an anomaly graph with anomaly detection and plot.

    Arguments:
    - data (pandas.DataFrame): The input data containing the 'times' and 'value_mean' columns.
    - times (str): The name of the time column in the data. Default is 'times'.
    - value_mean (str): The name of the value column in the data. Default is 'value_mean'.
    - period (int): The period of the data, which is the rolling window for the anomaly detection. 
         Default is 7.
    - iqr_alpha (float): The alpha value for the interquartile range. 
        Smaller IQR values will result in a lower threshold for detecting an anomaly. 
        Default is 0.05.
    - clean_alpha (float): The alpha value for the cleaning. Determines which values should be removed. 
        A smaller clean_alpha will result in more points being completely removed from the dataset. 
        Default is 0.75.

    Returns:
    - plotly.graph_objects.Figure: The plot object representing the anomaly graph.

    Raises:
    - ValueError: If the 'times' or 'value_mean' column does not exist in the data.
    - ValueError: If the 'times' column is not a string.
    - ValueError: If the 'value_mean' column is not a string.
    - ValueError: If the 'period' is not an integer.
    - ValueError: If the 'iqr_alpha' is not a float.
    - ValueError: If the 'clean_alpha' is not a float.

    """
   
    data_cleaned = data.dropna(subset=['value_mean'])

    anomalize_df = pytimetk.anomalize(
        data=data_cleaned,
        date_column='times',
        value_column='value_mean',
        period=period,
        iqr_alpha=iqr_alpha,
        clean_alpha=clean_alpha,
        clean="min_max"
    )

    decomp = pytimetk.plot_anomalies_decomp(
        data=anomalize_df,
        date_column='times',
        engine='plotly',
        title='Seasonal Decomposition'
    )

    return decomp


###########################################################################################
######### Streamlit #######################################################################
########################################################################################### 

## Configure the page 
st.set_page_config(page_title="Advanced Statistics", layout="wide")
st.title("Advanced Statistics") # Title for the streamlit app 

# Drop down menu for location
selected_location = st.selectbox("Select Location", ["TREQ Station", "Bay Bouy", "Beach 2 Tower", "Beach 2 Bouy", "Beach 6 Bouy", "Nearshore Bouy", "Walnut Creek Bouy"])

# Call your function to create the Leaflet map
leaflet_map = create_leaflet_map(selected_location)

# Display the Leaflet map using st.markdown
st.markdown(folium_static(leaflet_map), unsafe_allow_html=True)

### HARD CODE TO BRING IN THE DATA 
#file_path = "/Users/benjaminmakhlouf/Downloads/daily_tidy_all_data.csv"
#df = pd.read_csv(file_path)

## go the directory name 
dirname = os.path.dirname(__file__)

# Set location to correct frequency csv
#if frequency_selected == "Daily":
#    df = df_creation(dirname, "/daily_tidy_all_data.csv")
#else:
#    df = df_creation(dirname, "/hourly_tidy_all_data.csv")



### DOUBLE CHECK 
df['times'] = pd.to_datetime(df['times'])  # make sure times are in datetime
df['value_mean'] = pd.to_numeric(df['value_mean'])  # make sure value_mean is numeric

# Drop down menu for the user to choose the selected parameter, stored in selected_parameter 
selected_parameter = st.selectbox("Select Parameter", ["Air_Temperature", "Barometric_Pressure", "Daily_Rain"])

selected_parameter = "Air_Temperature"
print(df)

# create a new data frame that is the new selected parameter only 
df_param = df[df['parameter'] == selected_parameter]

print(df_param)
# Call the create_trendline function to create the trendline figure 
fig = create_trendline(df_param)

# pio.show(fig)
st.plotly_chart(fig)

fig2 = create_anomaly_graph(df_param)

st.plotly_chart(fig2)

dec = anomaly_decomp(df_param)

st.plotly_chart(dec)
