"Defines functions to run advanced time series statistics on selected values"

import pandas as pd
import plotly.io as pio
import pytimetk
import streamlit as st
import datetime
import numpy as np
#### 

def df_creation2(path_to_df: str) -> [pd.DataFrame(), str, list, str, str]:
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
    locations_selected_display = st.selectbox(
        "Data collection sites",
        sites_display_name
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

#######################################################################################################
##### Function to create the time series trendline 
#######################################################################################################

import pytimetk

def create_trendline(data):
    """
    Use pytimetk to create a non-linear trendline plot for the selected data

    Parameters:
    - data: pandas DataFrame
        Input data containing a 'times' column and a 'value_mean' column.

    Returns:
    - fig (plotly figure): figure of the trendline plot

    Raises:
    - ValueError: If 'data' is not a pandas DataFrame.
    - ValueError: If 'times' column is not present in 'data' 
    - ValueError: If 'value_mean' column is not present in 'data' 
    - ValueError: If 'times' column does not have at least 3 non-0 or non-NA values 
    - ValueError: If 'times' column is not a datetime object.
    """
    
    if not isinstance(data, pd.DataFrame):
        raise ValueError("'data' must be a pandas DataFrame.")
    
    if 'times' not in data.columns:
        raise ValueError("The 'times' column is not present in the data.")
    
    if 'value_mean' not in data.columns:
        raise ValueError("The 'value_mean' column is not present in the data.")
    
    if not pd.api.types.is_datetime64_any_dtype(data['times']):
        raise ValueError("The 'times' column must be a datetime object.")
    
    fig = pytimetk.plot_timeseries(
        data=data,
        date_column='times',
        value_column='value_mean'
    )
    
    return fig


###########################################
### function for anomaly calculation
###########################################


def create_anomaly_graph(data, period=7, iqr_alpha=0.05, clean_alpha=0.75):
    """
    Use pytimetk to plot a chosen variable over a selected time period, with statistical
    analysis to produce anomaly bars and display values considered as anomalies.

    Parameters:
    - data: pandas DataFrame
        Input data containing a 'times' column and a 'value_mean' column.
    - period: int, optional
        The time period for analysis. Default is 7.
    - iqr_alpha: float, optional
        The alpha level for the IQR-based anomaly detection. Default is 0.05.
    - clean_alpha: float, optional
        The alpha level for data cleaning. Default is 0.75.

    Returns:
    - anom_plot: Depends on the plotting engine used (e.g., plotly figure).

    Raises:
    - ValueError: If 'data' is not a pandas DataFrame.
    - ValueError: If 'times' column is not present in 'data'.
    - ValueError: If 'value_mean' column is not present in 'data'.
    - ValueError: If 'data' contains NaN values in the 'value_mean' column.
    - ValueError: If 'period' is not a positive integer.
    - ValueError: If 'iqr_alpha' is not between 0 and 1.
    - ValueError: If 'clean_alpha' is not between 0 and 1.
    - ImportError: If pytimetk is not installed.

"""
    if not isinstance(data, pd.DataFrame):
        raise ValueError("'data' must be a pandas DataFrame.")
    
    if 'times' not in data.columns:
        raise ValueError("The 'times' column is not present in the data.")
    
    if 'value_mean' not in data.columns:
        raise ValueError("The 'value_mean' column is not present in the data.")
    
    if not isinstance(period, int) or period <= 0:
        raise ValueError("'period' must be a positive integer.")
    
    if not (0 <= iqr_alpha <= 1):
        raise ValueError("'iqr_alpha' must be between 0 and 1.")
    
    if not (0 <= clean_alpha <= 1):
        raise ValueError("'clean_alpha' must be between 0 and 1.")
    

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

    anom_plot = pytimetk.plot_anomalies(
        data=anomalize_df,
        date_column='times',
        engine='plotly',
        title='Plot Anomaly Bands'
    )

    return anom_plot


#########################################################################################################
### Function for the statistical decomposition 
#########################################################################################################

def anomaly_decomp(data, period=7, iqr_alpha=0.05, clean_alpha=0.75):
    """
    Use pytimetk to plot statistical decomposition of anomaly calculation.

    Parameters:
    - data: pandas DataFrame
        Input data containing a 'times' column and a 'value_mean' column.
    - period: int, optional
        The time period for analysis. Default is 7.
    - iqr_alpha: float, optional
        The alpha level for the IQR-based anomaly detection. Default is 0.05.
    - clean_alpha: float, optional
        The alpha level for data cleaning. Default is 0.75.

    Returns:
    - decomp: figure with statistical decomposition of anomaly calculation

    Raises:
    - ValueError: If 'data' is not a pandas DataFrame.
    - ValueError: If 'times' column is not present in 'data'.
    - ValueError: If 'value_mean' column is not present in 'data'.
    - ValueError: If 'period' is not a positive integer.
    - ValueError: If 'iqr_alpha' is not between 0 and 1.
    - ValueError: If 'clean_alpha' is not between 0 and 1.
    """
    
    if not isinstance(data, pd.DataFrame):
        raise ValueError("'data' must be a pandas DataFrame.")
    
    if 'times' not in data.columns:
        raise ValueError("The 'times' column is not present in the data.")
    
    if 'value_mean' not in data.columns:
        raise ValueError("The 'value_mean' column is not present in the data.")
    
    if not isinstance(period, int) or period <= 0:
        raise ValueError("'period' must be a positive integer.")
    
    if not (0 <= iqr_alpha <= 1):
        raise ValueError("'iqr_alpha' must be between 0 and 1.")
    
    if not (0 <= clean_alpha <= 1):
        raise ValueError("'clean_alpha' must be between 0 and 1.")
    
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

#######
