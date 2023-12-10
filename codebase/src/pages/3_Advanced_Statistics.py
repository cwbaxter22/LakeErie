import os
import streamlit as st
import pandas as pd
import numpy as np
import pytimetk
import plotly.io as pio
import folium
import pathlib
#from streamlit_folium import folium_static
from frontend import df_manip_plotting
from frontend import leaflet_map
from frontend import anomaly


# Configure the page 
st.set_page_config(page_title="Advanced Statistics", layout="wide")
st.title("Advanced Statistics") # Title for the streamlit app

#### Bring in and filter the data frame based on user defined preferences 
# Relative path to /pages
codebase_path = pathlib.Path(__file__).parents[2]
data_path = str(codebase_path) + "/data/processed/combined/"
df, var_plot, loc_to_plot, start_date_to_plot, end_date_to_plot = anomaly.df_creation2(data_path)

### Create time series trendline plot 
st.title("Time series visualization with long term trend line")
st.write(
    "This dashboard displays long term data as well as a long term trendline. "
)

fig = anomaly.create_trendline(df)
st.plotly_chart(fig)

st.title("Anomaly Detection Dashboard")
st.write(
    "This dashboard visualizes anomalies in the selected data based on user-defined parameters."
)

period = st.number_input("Enter Period value", value=7, step=1)
IQR_alpha = st.number_input("Enter IQR alpha value", value=0.05, step=0.01)
Clean_alpha = st.number_input("Enter Clean alpha value", value =.75, step = .1)

#Create figure 2 , the anomaly detection. 
fig2 = anomaly.create_anomaly_graph(df,period,IQR_alpha,Clean_alpha)
st.plotly_chart(fig2)

if st.button("Show Statistical Decomposition"):
    # If the button is clicked, display Figure 3
    st.title("Statistical decomposition of time series statistics")
    st.write("add description here about what these graphs mean ")
    fig3 = anomaly.anomaly_decomp(df)
    st.plotly_chart(fig3)

if st.button("Show Selected Data"):
    # If the button is clicked, display the selected data frame
    st.write("Selected Data:")
    st.write(df)
