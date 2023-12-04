"""Simple module to provide brief overview of application

Overview is written in markdown.
Links to important sites are provided."""

import streamlit as st
st.title("About the application")
st.markdown(
    """
    B-ware is an open-source app built for the analysis
    of data collected from Buoys in Lake Erie.
    Data property of Regional Science Consortium.
    
    For current raw data, please visit [NextSens - WQDataLive](https://www.wqdatalive.com/)

    For application source code, please visit /
    [GitHub - LakeErie](https://github.com/Bware583/LakeErie)
    
    
    Created by Colin Baxter, Zac Espinosa, Ben Makhlouf, & Cole Morokhovich
    """
)
