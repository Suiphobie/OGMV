import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static

# Load the data
df = pd.read_csv('stationnement-velo-en-ile-de-france.csv', delimiter=';')

# Geocoding function to get latitude and longitude from address
def get_coordinates(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

# Function to create map and load nearby points
def create_map(lat, lon, data, radius=1, max_points=5):
    # Create a map centered around the coordinates with a closer zoom
    m = folium.Map(location=[lat, lon], zoom_start=20)

    # Calculate distances and sort points
    data['distance'] = data.apply(lambda row: haversine_distance(lat, lon, *map(float, row['geo_point_2d'].split(','))), axis=1)
    closest_points = data.sort_values(by='distance').head(max_points)

    # Add markers for the closest points with additional information
    for index, row in closest_points.iterrows():
        point_lat, point_lon = map(float, row['geo_point_2d'].split(','))
        popup_text = f"<br>Couvert: {row['couvert']}<br>Capacité {row['capacite']}<br>Acces: {row['acces']}<br>Payant: {row['payant']}<br>Surveiller: {row['surveille']}<br>Type: {row['type']}"
        folium.Marker([point_lat, point_lon], popup=popup_text).add_to(m)
    return m

# Haversine formula to calculate distance between two points on the earth
def haversine_distance(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, asin, sqrt
    R = 6371  # Radius of earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    return R * c

# Streamlit app
def main():
    st.title("Bicycle Parking Locations Near You")

    # Address input
    address = st.text_input("Enter an address to find nearby bicycle parking:")
    if address:
        lat, lon = get_coordinates(address)
        st_map = create_map(lat, lon, df)
        folium_static(st_map)

if __name__ == "__main__":
    main()
