import streamlit as st

st.set_page_config(layout="wide") # Page configuration must be first Streamlit command called
st.title("Advanced Statistical Analysis") # Page title

LOCATIONS = list(df['Location'].unique()) # List of all weather station locations
VARIABLES = list(df['variable'].unique()) # List of all variable types

with st.sidebar: # sidebar hides the drop-down
    st.subheader("Configure data selection")
    START_DATE = st.date_input("Choose start-date", min_value=datetime.date(2021, 7, 21), max_value=datetime.date(2023, 8, 1), value = None)
    END_DATE = st.date_input("Choose end-date", value = None)

    LOCATION = st.selectbox(label = "Choose a location", options = LOCATIONS)
    #Figure out how to make this multiselect work
    #LOCATION = st.multiselect('Choose desired locations', LOCATIONS)
    VARIABLE = st.selectbox(label = "Choose a variable", options = VARIABLES)

#Create temporary dataframe based on date range
mask = (df['Time'] > np.datetime64(START_DATE)) & (df['Time'] <= np.datetime64(END_DATE))
df_intime = df.loc[mask]

# Configure temporary dataframe to queried values
df_viz = df_intime.query(f"Location=='{LOCATION}'").query(f"variable=='{VARIABLE}'")

# Call the trendline function to create the figure
fig_trendline = trendline(df_viz)

# Display the trendline figure in the Streamlit app
st.plotly_chart(fig_trendline)

# Add Word documentation below the trendline figure
st.write("Time series data with trendline.")

# Call the anomaly function to create the figure
fig_anomaly = anomaly(df_viz)

# Display the anomaly figure in the Streamlit app
st.plotly_chart(fig_anomaly)

# Add Word documentation below the anomaly figure
st.write("Anomaly band display of chosen data.")

# Create a button to display the deconstruction figure
if st.button("Display Deconstruction"):
    # Call the deconstruct function to create the figure
    fig_deconstruction = deconstruct(df_viz)

    # Display the deconstruction figure in the Streamlit app
    st.plotly_chart(fig_deconstruction)
    