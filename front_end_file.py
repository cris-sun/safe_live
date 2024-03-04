import streamlit as st
import requests
import folium
from streamlit_folium import folium_static

def create_map(day, month, year):
    ''' Function to create basic map once date of visit has been input.''' # Currently the date has no bearing on the map...
    map = folium.Map(location=[34.052235, -118.243683], zoom_start=12)
    folium.Marker(location=[34.052235, -118.243683], popup='Los Angeles').add_to(map)
    folium_static(map)

def main():
    st.set_page_config(page_title="SafeLive Los Angeles", layout="wide", page_icon=":rocket:", initial_sidebar_state="expanded")
    st.title('Crime Map Visualization')
    st.write("Provide an explanation of the app and how to use it")
    st.markdown(
        """
        <style>
        .stForm {
            background-color: #383e42;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    day = st.slider('Select Day', 1, 31)
    month = st.selectbox('Select Month', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    year = st.slider('Select Year', 2000, 2025)

    # Display the map
    create_map(day, month, year)

response = requests.get(f'https://mvp-a32u27pqgq-ew.a.run.app').json

# Will need to be significantly amended once model purpose is defined

if __name__ == '__main__':
    main()
