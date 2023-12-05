"Defines functions to run advanced time series statistics on selected values"

import pandas as pd
import plotly.io as pio
import pytimetk

# TO ASK COLIN, how this will interact with "front front" end
# Read in Data csv
# Make sure time is datetime
# remove NA Values 
# Can only be ONE variable at a time for advanced stats 

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

    if 'times' not in data.columns or 'value_mean' not in data.columns:
        raise ValueError("The 'times' or 'value_mean' column does not exist in the data.")

    if data['times'].dtype != 'datetime64[ns]':
        raise ValueError("The 'times' column is not a datetime object.")

    if data['times'].empty or data['value_mean'].empty:
        raise ValueError("There is no data in either the 'times' or 'value_mean' column.")

    non_numeric_values = pd.to_numeric(data['value_mean'], errors='coerce').isnull()
    if non_numeric_values.any():
        invalid_rows = data[non_numeric_values].index.tolist()
        raise ValueError(f"There are non-numeric values in the 'value_mean' column. Invalid rows: {invalid_rows}")

    fig = pytimetk.plot_timeseries(
        data=data,
        date_column='times',
        value_column='value_mean'
    )
    
    return fig

def create_anomaly_graph(data, times, value_mean, period=7, iqr_alpha=0.05, clean_alpha=0.75):
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
    if 'times' not in data.columns or 'value_mean' not in data.columns:
        raise ValueError("The 'times' or 'value_mean' column does not exist in the data.")

    if data['times'].dtype != 'datetime64[ns]':
        raise ValueError("The 'times' column is not a datetime object.")

    if data['times'].empty or data['value_mean'].empty:
        raise ValueError("There is no data in either the 'times' or 'value_mean' column.")

    if not pd.to_numeric(data['value_mean'], errors='coerce').notnull().all():
        raise ValueError("There is a non-numeric value in the 'value_mean' column.")

    if not isinstance(period, (int, float)) or period < 0:
        raise ValueError("The 'period' argument must be a non-negative numeric value.")

    if not isinstance(iqr_alpha, (int, float)) or iqr_alpha < 0:
        raise ValueError("The 'iqr_alpha' argument must be a non-negative numeric value.")

    if not isinstance(clean_alpha, (int, float)) or clean_alpha < 0:
        raise ValueError("The 'clean_alpha' argument must be a non-negative numeric value.")

    anomalize_df = pytimetk.anomalize(
        data=data,
        date_column=times,
        value_column=value_mean,
        period=period,
        iqr_alpha=iqr_alpha,
        clean_alpha=clean_alpha,
        clean="min_max"
    )

    anomplot = pytimetk.plot_anomalies(
        data=anomalize_df,
        date_column=times,
        engine='plotly',
        title='Plot Anomaly Bands'
    )

    return anomplot

def anomaly_decomp(data, times='times', value_mean='value_mean', period=7, iqr_alpha=0.05, clean_alpha=0.75):
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
    if not isinstance(data, pd.DataFrame):
        raise ValueError("The 'data' argument must be a pandas DataFrame.")

    if not isinstance(times, str):
        raise ValueError("The 'times' argument must be a string.")

    if not isinstance(value_mean, str):
        raise ValueError("The 'value_mean' argument must be a string.")

    if not isinstance(period, int):
        raise ValueError("The 'period' argument must be an integer.")

    if not isinstance(iqr_alpha, float):
        raise ValueError("The 'iqr_alpha' argument must be a float.")

    if not isinstance(clean_alpha, float):
        raise ValueError("The 'clean_alpha' argument must be a float.")

    if times not in data.columns or value_mean not in data.columns:
        raise ValueError(f"The '{times}' or '{value_mean}' column does not exist in the data.")

    if data[times].dtype != 'datetime64[ns]':
        raise ValueError(f"The '{times}' column is not a datetime object.")

    if data[times].empty or data[value_mean].empty:
        raise ValueError(f"There is no data in either the '{times}' or '{value_mean}' column.")

    if not pd.to_numeric(data[value_mean], errors='coerce').notnull().all():
        raise ValueError(f"There is a non-numeric value in the '{value_mean}' column.")

    anomalize_df = pytimetk.anomalize(
        data=data,
        date_column=times,
        value_column=value_mean,
        period=period,
        iqr_alpha=iqr_alpha,
        clean_alpha=clean_alpha,
        clean="min_max"
    )

    decomp = pytimetk.plot_anomalies_decomp(
        data=anomalize_df,
        date_column=times,
        engine='plotly',
        title='Seasonal Decomposition'
    )

    return decomp
