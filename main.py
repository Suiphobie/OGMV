import streamlit as st
import pandas as pd
import folium
from geopy.geocoders import Nominatim
from streamlit_folium import folium_static

# Load the data
df = pd.read_csv(
    'OGMV\stationnement-velo-en-ile-de-france.csv', delimiter=';')

# Geocoding function to get latitude and longitude from address


def get_coordinates(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

# Function to create map and load nearby points


def create_map(lat, lon, data, radius=1):
    # Create a map centered around the coordinates
    m = folium.Map(location=[lat, lon], zoom_start=14)

    # Add markers within the specified radius (in kilometers)
    for index, row in data.iterrows():
        point_lat, point_lon = map(float, row['geo_point_2d'].split(','))
        if haversine_distance(lat, lon, point_lat, point_lon) <= radius:
            folium.Marker([point_lat, point_lon]).add_to(m)
    return m

# Haversine formula to calculate distance between two points on the earth


def haversine_distance(lat1, lon1, lat2, lon2):
    from math import radians, cos, sin, asin, sqrt
    R = 6371  # Radius of earth in kilometers

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * \
        cos(radians(lat2)) * sin(dlon/2)**2
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
