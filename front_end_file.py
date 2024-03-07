import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import altair as alt


st.set_page_config(
    page_title="SafeLive Los Angeles",
    layout="wide",
    page_icon=":rocket:",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")
st.markdown(
    """
    <style>
    body {
        background-color: #1E1E1E;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)


#######################
# Sidebar
with st.sidebar:
    st.title('Additional Feature Selection')



def create_map(age, latitude, longitude, day_ocurred, month_ocurred, year_ocurred):
    ''' Function to create basic map once date of visit has been input.''' # Currently the date has no bearing on the map...
    map = folium.Map(location=[34.052235, -118.243683], zoom_start=10)
    folium.Marker(location=[latitude, longitude], popup='Your intended location').add_to(map)
    folium_static(map)


def main():
    st.title('SafeLive - A crime prediction app')
    st.write("Welcome to our Crime Prediction App for Los Angeles! With just a few inputs — your age, location, and date of visit — we'll provide you with insights into the most likely crime you might encounter during your time in LA. Our app utilizes advanced data analytics and machine learning algorithms to offer personalized crime predictions, helping you stay informed and make informed decisions while exploring the city.")

    #################### Feature inputs ########################################
    age = st.selectbox("Select your age:", range(18,100))
    latitude = st.slider('Select latitude', 33.699, 34.337, (33.699 + 34.337) / 2)
    longitude = st.slider('Select longitude:', -117.656, -118.669, (-117.656 + -118.669) / 2)
    day_ocurred = st.slider('Select Day of your visit', 1, 31)
    month_ocurred = st.selectbox('Select Month of your visit', range(1, 13))
    year_ocurred = st.slider('Select Year of your visit', 2020, 2025)

    # Display the map
    create_map(age, latitude, longitude, day_ocurred, month_ocurred, year_ocurred)

    response = requests.get(f"https://mvp-a32u27pqgq-ew.a.run.app/predict?victim_age={age}&latitude={latitude}&longitude={longitude}&day_ocurred={day_ocurred}&month_ocurred={month_ocurred}&year_ocurred={year_ocurred}").json()

    st.write("Hmm... the biggest risk posed to your visit is", response)
# Will need to be significantly amended once model purpose is defined

if __name__ == '__main__':
    main()
