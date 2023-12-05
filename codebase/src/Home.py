"""Module that generates landing page for application

This page is mainly an image."""

import base64
import os
import streamlit as st

def get_base64(bin_file: str) ->base64:
    """
    Generate base64 coding to use for background image.
    Function courtesy of:
    https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067
    https://stackoverflow.com/questions/72582550/how-do-i-add-background-image-in-streamlit

    Arguments:
    ----------
    bin_file (str): bin file for image

    Returns:
    ----------
    base64 (str): encoded location

    """
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
def set_background(img_file) -> None:
    """
    Set background image using file link and base 64 encoding.
    Function courtesy of:
    https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067
    https://stackoverflow.com/questions/72582550/how-do-i-add-background-image-in-streamlit

    Arguments:
    ----------
    img_file (str): image location

    Returns:
    ----------
    None

    """

    bin_str = get_base64(img_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)
st.set_page_config(
    page_title="Home",
    page_icon="🌊"
)
# Create path to file
home_path = os.path.dirname(__file__)
# Merge path to file with image name
background_image_path = home_path + '/PresqueIsle.jpg'
set_background(background_image_path)
=======
home_path = os.path.dirname(__file__)
background_image_path = home_path+'/PresqueIsle.jpg'
set_background(background_image_path)
st.sidebar.success("Menu")
st.title("B-ware")
st.sidebar.success("Menu")
st.markdown(
    """
        :green[Buoy-Water Analysis Reporting Environment]
    """
)
