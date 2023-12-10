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

# Relative path to /pages
codebase_path = pathlib.Path(__file__).parents[2]
data_path = str(codebase_path) + "/data/processed/combined/"
df, var_plot, loc_to_plot, start_date_to_plot, end_date_to_plot = anomaly.df_creation2(data_path)


fig = anomaly.create_trendline(df)
st.plotly_chart(fig)

st.title("Anomaly Detection Dashboard")
st.write(
    "This dashboard visualizes anomalies in the selected data based on user-defined parameters."
)

period = st.number_input("Enter Period value", value=1.5, step=0.1)
IQR_alpha = st.number_input("Enter IQR alpha value", value=0.05, step=0.01)
Clean_alpha = st.number_input("Enter Clean alpha value", value =.05, step = .01)
fig2 = anomaly.create_anomaly_graph(df)
st.plotly_chart(fig2)

