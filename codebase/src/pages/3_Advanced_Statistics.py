import os
import streamlit as st
import pandas as pd
import numpy as np
import pytimetk
import plotly.io as pio
import folium
import pathlib
from streamlit_folium import folium_static

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

folium_map = leaflet_map.map_main(loc_to_plot)
folium_static(folium_map)

### Create time series trendline plot 
st.title("Time series visualization with long term trend line")
st.write(
    "This dashboard displays long term data as well as a long term trendline. "
)

fig = anomaly.create_trendline(df)
st.plotly_chart(fig)

if st.button("Show Selected Data"):
    # If the button is clicked, display the selected data frame
    st.write("Selected Data:")
    st.write(df)


st.title("Anomaly Detection Dashboard")
st.write(
    "This dashboard visualizes anomalies in the selected data. "
    "Adjust parameters to change the anomaly calculation."
)

# Parameter Descriptions
st.markdown(''':blue[Period: The period is the window size for analyzing anomalies. 
                This value should be adjusted to represent an appropriate time period 
                for analyzing your data based on the amount of time selected to be analyzed]''')

period = st.number_input("Enter Period value", value=7, step=1)

st.markdown(''':blue[IQR alpha: controls the threshold for detecting outliers by setting the 
                significance level used in the interquartile method for outlier detection. 
                The default value is .05, or a 5% significance level. 
                Lowering this number will result in a higher threshold, 
                which means less values will be considered to be outliers. ]''')
IQR_alpha = st.number_input("Enter IQR alpha value", value=0.05, step=0.01)

st.markdown(''':blue[Clean alpha: The Clean alpha value sets the threshold for removing outliers in the data. 
                A higher alpha level decreases the sensitivity]''')

Clean_alpha = st.number_input("Enter Clean alpha value", value=0.75, step=0.1)


#Create figure 2 , the anomaly detection. 
fig2 = anomaly.create_anomaly_graph(df,period,IQR_alpha,Clean_alpha)
st.plotly_chart(fig2)

if st.button("Show Statistical Decomposition"):
    # If the button is clicked, display Figure 3
    st.title("Statistical decomposition of time series statistics")
    st.write("The time series data is decomposed into several components, which include:")
    st.markdown(''':blue[*Observed*: Actual time series data]''')
    st.markdown(''':blue[*Trend*: Underlying pattern or direction in the data over time]''')
    st.markdown(''':blue[*Seasonal*: Trends in reoccuring cycles over the specified period]''')
    st.markdown(''':blue[*Residual*: Residual represents what patterns are left unexplained in the data after trend and seasonal components have been removed from observed]''')
    fig3 = anomaly.anomaly_decomp(df,period,IQR_alpha,Clean_alpha)
    st.plotly_chart(fig3)

