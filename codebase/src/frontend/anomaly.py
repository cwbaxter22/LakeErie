"Defines functions to run advanced time series statistics on selected values"

import pandas as pd
import plotly.io as pio
import pytimetk

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
    
    if data['times'].count() < 3 or data['value_mean'].count() < 3:
        raise ValueError("Each column must have at least 3 non-0 or non-NA values.")
    
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
