import streamlit as st
import base64

# https://discuss.streamlit.io/t/how-do-i-use-a-background-image-on-streamlit/5067
# https://stackoverflow.com/questions/72582550/how-do-i-add-background-image-in-streamlit
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()
def set_background(png_file):
    bin_str = get_base64(png_file)
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
    page_icon="👋"
)
set_background("PresqueIsle.jpg")
st.sidebar.success("Menu")
st.title("B-ware")
st.markdown(
    """
        :green[Buoy-Water Analysis Reporting Environment]
    """
)

