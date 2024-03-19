#-------------------------------------------------------------------#
# Libraries

# Calculus
import pandas as pd
import os
import geopandas as gpd
import pandas as pd

#-------------------------------------------------------------------#
# Functions

# generating a gravity score
def assign_gravity(crime_description):
    lower_case_description = crime_description.lower()
    if any(word in lower_case_description for word in ['petty theft', 'vandalism', 'minor fraud', 'trespass','stole']):
        return 1  # Low Gravity
    elif any(word in lower_case_description for word in ['burglary', 'serious fraud', 'aggravated assault', 'robbery']):
        return 2  # Medium Gravity
    elif any(word in lower_case_description for word in ['homicide', 'rape', 'kidnapping', 'arson','dead','penetration','penis','child pornography']):
        return 3  # High Gravity
    else:
        return 1 # Default to Low Gravity if not clearly fitting other categories

# adding the geoshape data
def data_enriching(csv_file):
    current_dir = os.getcwd()
    current_dir

    file_path = os.path.join(current_dir, '..', 'raw_data', csv_file)
    df = pd.read_csv(file_path)

    columns_keep = [
'division_number',
'date_reported',
'date_occurred',
'area',
'area_name',
'reporting_district',
'part',
'crime_code',
'crime_description',
'modus_operandi',
'victim_age',
'victim_sex',
'victim_descent',
'premise_code',
'premise_description',
'weapon_code',
'weapon_description',
'status',
'status_description',
'crime_code_1',
'crime_code_2',
'crime_code_3',
'crime_code_4',
'location',
'cross_street',
'latitude',
'longitude',
]

    df = df[columns_keep]
    df['counter']=1

    # Dates
    df['date_occurred'] = pd.to_datetime(df['date_occurred'], errors='coerce')
    df['year_occurred'] = df['date_occurred'].dt.year
    df['month_occurred'] = df['date_occurred'].dt.month
    df['hour_occurred'] = df['date_occurred'].dt.hour

    # Load the shapefile

    #   fetch all the data from the raw_data folder

    file_path = os.path.join(current_dir, '..', 'data','geo_data','cfbcc20d-2c5d-4c30-9dfa-627d46ec1a742020328-1-9ulknm.pzqsm.shp')

    neighborhoods = gpd.read_file(file_path)

    crime_data_gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    crime_data_gdf.set_crs(neighborhoods.crs, inplace=True).head(1)

    joined_gdf = gpd.sjoin(crime_data_gdf, neighborhoods, how='left', op='within')

    joined_gdf['gravity_for_tourist'] = joined_gdf['crime_description'].apply(assign_gravity)

    return joined_gdf
