import streamlit as st
import requests
import folium
from streamlit_folium import folium_static
import altair as alt
import geopandas as gpd
import pandas as pd


import plotly.express as px


# Personal library #
import sys
import os

# Path to the folder containing the pesonalized functions
folder_path = os.path.abspath(os.path.join( 'library'))
sys.path.insert(0, folder_path)

# Now you can import your module or functions
import la_functions as la



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

def create_map(age, sex, area, day_occurred, month_occurred, year_occurred):
    ''' Function to create basic map once features have been input.'''
    map = folium.Map(location=[34.052235, -118.243683], zoom_start=10)
    #folium.Marker(location=[latitude, longitude], popup='Your intended location').add_to(map)
    gdf = gpd.read_file('data/LAPD_Division/LAPD_Divisions.shp')
    #gdf = gpd.read_file('data/geo_data/cfbcc20d-2c5d-4c30-9dfa-627d46ec1a742020328-1-9ulknm.pzqsm.shp')

    def style_function(feature):
        if feature['properties'].get('PREC', 'Unknown Area') == area:
            # Style for the selected area
            return {
                'fillColor': '#7CFC00',  # A bright color for the selected area
                'color': 'green',  # Border color for the selected area
                'weight': 3,
                'dashArray': '1, 1',
                'fillOpacity': 0.7,
            }
        else:
            # Default style for other areas
            return {
                'fillColor': '#5d6fb3',
                'color': 'grey',
                'weight': 2,
                'dashArray': '5, 5',
                'fillOpacity': 0.5,
            }

    folium.GeoJson(
        gdf,
        name='geojson',
        style_function=style_function
    ).add_to(map)

    folium.LayerControl().add_to(map)


    folium_static(map)

def create_map_with_predictions(age, sex, area, day_occurred, month_occurred, year_occurred):
    map_pred = folium.Map(location=[34.052235, -118.243683], zoom_start=10)
    risk_to_color = {'1': '#green', '2': '#orange', '3': '#red'}
    gdf = gpd.read_file('data/geo_data/cfbcc20d-2c5d-4c30-9dfa-627d46ec1a742020328-1-9ulknm.pzqsm.shp')
    gdf['color'] = gdf['name'].apply(lambda x: risk_to_color.get(response.get(x, 'Low'), '#grey'))  # Default to 'Low' or another category as fallback
    response = requests.get(f"https://mvp-a32u27pqgq-ew.a.run.app/predict?area={area}&victim_age={age}&year_occurred={year_occurred}&month_occurred={month_occurred}&day_occurred={day_occurred}&victim_sex={sex}").json()
    def outline(feature):
        return {
            'fillColor': feature['properties']['color'],
            'color': 'black',
            'weight': 2,
            'dashArray': '5, 5',
            'fillOpacity': 0.5,
        }
    folium.GeoJson(
        gdf,
        name='geojson',
        style_function=outline,
        tooltip=folium.GeoJsonTooltip(fields=['name']),
        popup=folium.GeoJsonPopup(fields=['name'])
    ).add_to(map_pred)

    folium.LayerControl().add_to(map_pred)

    # Display map in Streamlit
    folium_static(map_pred)

def threat_description(response):
    if response == 1:
        return f'The predicted likely crime category for someone of your profile in this area is {response["prediction"]}. These crimes are categorised as less serious and include petty theft and vandalism'
    if response == 2:
        return f'The predicted likely crime category for someone of your profile in this area is {response["prediction"]}. These crimes are categorised as of moderate seriousness and include aggrevated assault and robbery'
    if response == 3:
        return f'The predicted likely crime category for someone of your profile in this area is {response["prediction"]}. These crimes are categorised as very serious and include murder and rape. You should not visit this area at this time.'

def dummy_description(response):
    return f'The predicted crime category of someone of your profile is {response["prediction"]}. Crime categories are scored from 1-3, with 3 being the most serious'

######################################################

def top_5_grap(area):
    df = la.data_enriching2('data.csv')
    # Assuming fd.df_top_5(df, 'southwest') returns the desired DataFrame and is stored in `df_filtered`
    df_filtered = la.df_top_5(df, area).sort_values(by='counter')

    fig = px.bar(df_filtered, y='crime_description', x='counter')

    # Update layout for dark mode
    fig.update_layout({
    'plot_bgcolor': 'rgba(0, 0, 0, 0)',
    'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    'font_color': 'white',
    'title':'TOP 5 crimes in the area',
    'title_font_color': 'white',
    'xaxis': {'title': {'text': 'Counter', 'font': {'color': 'white'}},
              'color': 'white',
              'tickfont': {'color': 'white'}},
    'yaxis': {'title': {'text': 'Crime Description', 'font': {'color': 'white'}},
              'color': 'white',
              'tickfont': {'color': 'white'}},
})

    # Set dark axis lines
    fig.update_xaxes(showline=True, linewidth=2, linecolor='white', gridcolor='grey')
    fig.update_yaxes(showline=True, linewidth=2, linecolor='white', gridcolor='grey')

    return fig

def monthly_crimes(name):
    df = la.data_enriching2('data.csv')
    df['counter'] = 1
    filtered_df = df[(df['area_name'].str.lower() == name.lower()) & (df['year_occurred'] >= 2021)]

    # Create a pivot table to sum the 'counter' values by 'month_occurred' and 'year_occurred'
    pivot_table = filtered_df.pivot_table(index=['month_occurred', 'year_occurred'],
                                      values='counter', aggfunc='sum').reset_index()

    fig = px.line(pivot_table, x="month_occurred", y="counter",
              title='Monthly Crime Count in Foothill',
              line_shape='spline',
              color='year_occurred',  # This automatically assigns one color per year
              markers=True)

    # Update layout for dark mode
    fig.update_layout({
    'plot_bgcolor': 'rgba(17, 17, 17, 1)',
    'paper_bgcolor': 'rgba(17, 17, 17, 1)',
    'font_color': 'white',
    'title_font_color': 'white',
    'xaxis': {
        'title': {'text': 'Month Occurred', 'font': {'color': 'white'}},
        'color': 'white',
        'tickfont': {'color': 'white'},
        'showgrid': True, 'gridwidth': 1, 'gridcolor': 'DarkGrey'
    },
    'yaxis': {
        'title': {'text': 'Number of Crimes', 'font': {'color': 'white'}},
        'color': 'white',
        'tickfont': {'color': 'white'},
        'showgrid': True, 'gridwidth': 1, 'gridcolor': 'darkgrey'
    },
    'legend_title_text': 'Year',
    'legend_title_font_color': "white"
})
    return fig


######################################################


def main():
    st.title('SafeLive - Your Guardian in the Urban Jungle')
    st.write("Welcome to our Crime Prediction App for Los Angeles! With just a few inputs — including your age, location, and date of visit — we'll provide you with insights risks you might encounter during your time in LA. Our app utilizes advanced data analytics and machine learning algorithms to offer personalized crime predictions, helping you stay informed and make informed decisions while exploring the city.")

    age = st.sidebar.selectbox("Select your age:", range(18,100))

    sex_options = ['Male', 'Female', 'Transgender']
    sex_input = st.sidebar.selectbox('Select your Sex', sex_options)
    victim_sex_mapping = {'Female': [1, 0, 0], 'Male': [0, 1, 0], 'Transgender': [0, 0, 1]}
    sex = victim_sex_mapping.get(sex_input, [0, 0, 0])

    #area = st.sidebar.selectbox("Which area do you want to visit?")
    area_options = ['MISSION','DEVONSHIRE','FOOTHILL','TOPANGA','WEST VALLEY','NORTH HOLLYWOOD','VAN NUYS','NORTHEAST','HOLLYWOOD','WEST LOS ANGELES','HOLLENBECK','RAMPART','WILSHIRE','OLYMPIC','SOUTHWEST','NEWTON','PACIFIC','77TH STREET','SOUTHEAST','HARBOR','CENTRAL']
    area_input = st.sidebar.selectbox("Select the area of your visit", area_options)
    area_mapping = {'MISSION' : 1, 'DEVONSHIRE' : 2, 'FOOTHILL' : 3, 'TOPANGA' : 4, 'WEST VALLEY' : 5, 'NORTH HOLLYWOOD' : 6, 'VAN NUYS' : 7, 'NORTHEAST' : 8, 'HOLLYWOOD' : 9, 'WEST LOS ANGELES' : 10, 'HOLLENBECK' : 11, 'RAMPART' : 12, 'WILSHIRE' : 13, 'OLYMPIC' : 14, 'SOUTHWEST' : 15, 'NEWTON' : 16, 'PACIFIC' : 17, '77TH STREET' : 18, 'SOUTHEAST' : 19, 'HARBOR' : 20, 'CENTRAL' : 21}
    area = area_mapping.get(area_input)


    day_occurred = st.sidebar.slider('Select Day of your visit', 1, 31)
    month_occurred = st.sidebar.selectbox('Select Month of your visit', range(1, 13))
    year_occurred = st.sidebar.slider('Select Year of your visit', 2020, 2025)

    neighbourhood_options = ['Exposition Park', 'Downtown', 'Valley Village', 'Panorama City',
       'Chinatown', 'Granada Hills', 'Sylmar', 'Glassell Park',
       'Harbor City', 'Van Nuys', 'Encino', 'Tarzana', 'Griffith Park',
       'Brentwood', 'Pico-Robertson', 'Beverly Grove', 'Sawtelle',
       'Venice', 'Westlake', 'Vermont Knolls', 'Lincoln Heights',
       'Boyle Heights', 'Silver Lake', 'Mid-City', 'West Adams',
       'Broadway-Manchester', 'Hollywood', 'Mar Vista', 'Florence',
       'Mid-Wilshire', 'Baldwin Hills/Crenshaw', 'Vermont Square',
       'San Pedro', 'Watts', 'West Los Angeles', 'Westwood', 'Sun Valley',
       'Beverly Crest', 'Fairfax', 'Highland Park', 'Chesterfield Square',
       'East Hollywood', 'El Sereno', 'Elysian Park', 'Hansen Dam',
       'Reseda', 'Koreatown', 'Echo Park', 'Wilmington', 'Hyde Park',
       'Valley Glen', 'Northridge', 'Los Feliz', 'Cheviot Hills',
       'University Park', 'Leimert Park', 'Winnetka', 'Central-Alameda',
       'Sherman Oaks', 'Eagle Rock', 'Vermont-Slauson',
       'Lake Balboa', 'Harbor Gateway', 'Montecito Heights',
       'North Hills', 'Del Rey', 'Jefferson Park', 'Pico-Union',
       'Hollywood Hills', 'Atwater Village', 'Green Meadows', 'Pacoima',
       'Harvard Park', 'Hollywood Hills West', 'Century City',
       'Hancock Park', 'North Hollywood', 'Larchmont', 'Canoga Park',
       'Westchester', 'Manchester Square', 'Sunland', 'Arleta',
       'Mission Hills', 'Studio City', 'Vermont Vista', 'Harvard Heights',
       'Arlington Heights', 'Porter Ranch', 'Pacific Palisades',
       'South Park', 'Palms', 'Woodland Hills', 'Adams-Normandie',
       'Toluca Lake', 'Carthay', 'West Hills', 'Historic South-Central',
       'Cypress Park', 'Sepulveda Basin', 'Mount Washington',
       'Playa del Rey', 'Chatsworth', 'Playa Vista', 'Elysian Valley',
       'Windsor Square', 'Gramercy Park', 'Tujunga', 'Rancho Park',
       'Lake View Terrace', 'Bel-Air', 'Shadow Hills', 'Beverlywood',
       'Chatsworth Reservoir']
    #neigbourhood = st.sidebar.selectbox('Select the neighbourhood you will be visiting', neighbourhood_options)

    time_of_day_options = ['morning', 'afternoon', 'evening', 'night']

    ################################## Victim Descent ###############################################
    #descent_options = ['Other Asian', 'Black',  'Chinese', 'Cambodian', 'Filipino', 'Guamanian' , 'Hispanic/Latin/Mexican', 'American Indian/Alaskan Native', 'Japanese', 'Korean', 'Laotian', 'Other', 'Pacific Islander', 'Samoan', 'Hawaiian', 'Vietnamese', 'White',  'Asian Indian']
    #descent_input = st.sidebar.selectbox('Select your descent', descent_options)
    #victim_descent_mapping  = {'Other Asian': 'A', 'Black' : 'B',  'Chinese' : 'C', 'Cambodian' : 'D', 'Filipino' : 'F', 'Guamanian' : 'G', 'Hispanic/Latin/Mexican' : 'H', 'American Indian/Alaskan Native' : 'I',
    #                           'Japanese' : 'J', 'Korean' : 'K', 'Laotian' : 'L' , 'Other' : 'O', 'Pacific Islander' : 'P', 'Samoan' : 'S', 'Hawaiian' : 'U', 'Vietnamese' : 'V', 'White' : 'W',  'Asian Indian' : 'Z'}
    #victim_descent = victim_descent_mapping.get(descent_input)

    col1, col2,col3 = st.columns(3)

    with col1:
        st.header("Crime Prediction Map")
        create_map(age, sex, area, day_occurred, month_occurred, year_occurred)

    with col2:
        st.header("Prediction Dashboard")
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
        ### Statistics ###
        st.write(f"""
        Statistics related to the area : {area_input}
                 """)
        st.plotly_chart(top_5_grap(area_input) )
        
    with col3:
        st.header(f"Crime evolutions in {area_input}")
         ### Statistics ###
        fig = monthly_crimes(area_input)
        st.plotly_chart(fig, use_container_width=True)



if __name__ == '__main__':
    main()
