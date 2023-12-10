"""Generate web interface for users to view buoy and site variable data

Users will be prompted to choose location(s), variable, start time, and end time."""

import pathlib
import logging
import streamlit as st

# Note: For this import to work,
# the 2_Temporal_Data.py module needs to be run from a file within the src folder
from frontend import df_manip_plotting

# Initial Streamlit page setup
# Page configuration must be first Streamlit command called
st.set_page_config(layout="wide")
st.title("Historical Buoy Data")
# Relative path to /pages
codebase_path = pathlib.Path(__file__).parents[2]
DATA_PATH = str(codebase_path) + "/data/processed/combined/"
try:
    (df_viz,
     var_plot,
     loc_to_plot,
     start_date_to_plot,
     end_date_to_plot) = df_manip_plotting.df_creation(DATA_PATH)
except Exception as e:
    logging.exception(e)
    st.write("Unable to generate data based on these selections. \
          Please update input or refresh the page.")
try:
    # Choose between either chronological or annual comparison view
    data_comparison_type = st.radio(
    "Choose graph type",
    ["Chronological",
        "Annual Comparison"],
    captions = ["View chronology of chosen variable at one or more locations from "
                "selected start to end date",
                "Compare annual trends for one variable at one location."])
    error_bars_on = st.toggle("Display error bars")
    if data_comparison_type == "Chronological":
        fig = df_manip_plotting.create_all_time_fig(df_viz,
                                    "Chronological Timeline",
                                    var_plot,
                                    error_bars_on,
                                    loc_to_plot,
                                    start_date_to_plot,
                                    end_date_to_plot)
        df_manip_plotting.plot_it(fig, df_viz)
    else:
        # Generate annual data overlap
        an_fig = df_manip_plotting.create_annual_comparison_fig(df_viz,
                                "Annual Data Comparison",
                                var_plot,
                                error_bars_on,
                                loc_to_plot)
        df_manip_plotting.plot_it(an_fig, df_viz)
# Since the goal is to capture all exceptions, this warning is disabled.
except: # pylint: disable=bare-except
    st.write(":red[Unable to plot data]")
    st.write("Please confirm data selections have been made.\
             If all fields have been selected, data may not be available for these criteria.")
