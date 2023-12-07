"Defines functions to run advanced time series statistics on selected values"

import pandas as pd
import plotly.io as pio
import pytimetk

#################################
###### FUNCTIONS
# ############################### 

#######################################################################################################
####### Function to create dataframe #######
#######################################################################################################

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

#######################################################################################################
##### Function to create the time series trendline 
#######################################################################################################


def create_trendline(data):
    """
    Use pytimetk to create a non-linear trendline plot for the selected data

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


#########################################################################################################
### Function for the statistical decomposition 
#########################################################################################################


def anomaly_decomp(data, period=7, iqr_alpha=0.05, clean_alpha=0.75):
    """
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
