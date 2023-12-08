import os
import streamlit as st
import pandas as pd
import numpy as np
import pytimetk
import plotly.io as pio
import folium
from streamlit_folium import folium_static


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
