import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import altair as alt
import geopandas as gpd

################################################ Page setup ########################################################
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

def create_map(age, latitude, longitude, day_ocurred, month_ocurred, year_ocurred):
    ''' Function to create basic map once features have been input.'''
    map = folium.Map(location=[34.052235, -118.243683], zoom_start=10)
    #folium.Marker(location=[latitude, longitude], popup='Your intended location').add_to(map)
    gdf = gpd.read_file('data/LAPD_Division/LAPD_Divisions.shp')
    #gdf = gpd.read_file('data/geo_data/cfbcc20d-2c5d-4c30-9dfa-627d46ec1a742020328-1-9ulknm.pzqsm.shp')
    def style_function(feature):
        return {
            'fillColor': '#ffff00',
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0.5,
            'tooltip': feature['properties']['APREC'],
            'popup': feature['properties']['APREC']
        }

    folium.GeoJson(
        gdf,
        name='geojson',
        style_function=style_function
    ).add_to(map)

    folium.LayerControl().add_to(map)

    folium.GeoJson(gdf).add_to(map)
    folium_static(map)

def threat_description(response):
    if response == 1:
        return f'The predicted likely crime category for someone of your profile in this area is {response["prediction"]}. These crimes are categorized as less serious and include petty theft and vandalism'
    if response == 2:
        return f'The predicted likely crime category for someone of your profile in this area is {response["prediction"]}. These crimes are categorized as of moderate seriousness and include aggravated assault and robbery'
    if response == 3:
        return f'The predicted likely crime category for someone of your profile in this area is {response["prediction"]}. These crimes are categorized as very serious and include murder and rape. You should not visit this area at this time.'

def dummy_description(response):
    return f"""
The predicted crime category of someone of your profile is {response["prediction"]}.
Crime categories are scored from 1-3, with 3 being the most serious
"""

def main():
    st.title('SafeLive - A crime prediction app')
    st.write("Welcome to our Crime Prediction App for Los Angeles! With just a few inputs — your age, location, and date of visit — we'll provide you with insights into the most likely crime you might encounter during your time in LA. Our app utilizes advanced data analytics and machine learning algorithms to offer personalized crime predictions, helping you stay informed and make informed decisions while exploring the city.")

    age = st.sidebar.selectbox("Select your age:", range(18,100))
    sex_options = ['Male', 'Female', 'Transgender']
    sex_input = st.sidebar.selectbox('Select your Sex', sex_options)
    victim_sex_mapping = {'Female': [1, 0, 0], 'Male': [0, 1, 0], 'Transgender': [0, 0, 1]}
    sex = victim_sex_mapping.get(sex_input, [0, 0, 0])
    #area = st.sidebar.selectbox("Which area do you want to visit?")
    area = st.sidebar.selectbox("Select the area of your visit", range(1, 22))
    day_occurred = st.sidebar.slider('Select Day of your visit', 1, 31)
    month_occurred = st.sidebar.selectbox('Select Month of your visit', range(1, 13))
    year_occurred = st.sidebar.slider('Select Year of your visit', 2020, 2025)

    create_map(age, sex, area, day_occurred, month_occurred, year_occurred)

    if st.sidebar.button('Submit'):
            # Make API call to get prediction
            response = requests.get(f"https://mvp-a32u27pqgq-ew.a.run.app/predict?area={area}&victim_age={age}&year_occurred={year_occurred}&month_occurred={month_occurred}&day_occurred={day_occurred}&victim_sex={sex}").json()
            text = dummy_description(response)
            colour = '#808080'
            coloured_box_html = f"""
                <div style="background-color: {colour}; padding: 10px; border-radius: 5px; max-width: 800px">
                    <span style="color: white; font-weight: bold;">{text}</span>
                </div>
            """
            st.markdown(coloured_box_html, unsafe_allow_html=True)

            # Styling for map container
            st.markdown("""
            <style>
            .map-container {
                display: flex;
                justify-content: center;
                align-items: center;
                width: 800px;
                height: 600px;
            }
            </style>
            """, unsafe_allow_html=True)

if __name__ == '__main__':
    main()
