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

# Function to filter the data based on user selection
def filter_data(data, couvert, acces, payant, surveille, types):
    if couvert:
        data = data[data['couvert'] == couvert]
    if acces:
        data = data[data['acces'] == acces]
    if payant:
        data = data[data['payant'] == payant]
    if surveille:
        data = data[data['surveille'] == surveille]
    if types:
        data = data[data['type'].isin(types)]
    return data

# Function to create map and load nearby points
def create_map(lat, lon, data, radius=1, max_points=5, user_location=None):
    # Create a map centered around the coordinates with a closer zoom
    m = folium.Map(location=[lat, lon], zoom_start=20)
    
    # Add a red marker for the user's location if it is provided
    if user_location:
        folium.Marker(
            user_location,
            icon=folium.Icon(color="red", icon="info-sign"),
            popup="Vous êtes ici !"
        ).add_to(m)

    # Calculate distances and sort points
    data['distance'] = data.apply(lambda row: haversine_distance(lat, lon, *map(float, row['geo_point_2d'].split(','))), axis=1)
    filtered_points = data[data['distance'] <= radius].sort_values(by='distance').head(max_points)

    # Add markers for the filtered points with additional information and emoji
    for index, row in filtered_points.iterrows():
        point_lat, point_lon = map(float, row['geo_point_2d'].split(','))
        popup_text = f"""
        <b>🛖 Couvert:</b> {row['couvert']}<br>
        <b>🔓 Acces:</b> {row['acces']}<br>
        <b>💰 Payant:</b> {row['payant']}<br>
        <b>👁️ Surveiller:</b> {row['surveille']}<br>
        <b>🅿️ Type:</b> {row['type']}
        """
        folium.Marker([point_lat, point_lon], popup=folium.Popup(popup_text, max_width=300)).add_to(m)
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
    st.title("Où garer mon Velo")

    # Address input at the top
    address = st.text_input("Entrer une adresse en Île-de-France", key='address')

    # Radius and max points selection
    radius = st.slider("Sélectionnez un rayon en Km (max 5km)", min_value=0.5, max_value=5.0, value=1.0, step=0.1, key='radius')
    max_points = st.number_input("Sélectionnez le nombre d'abri à afficher (max 20)", min_value=1, max_value=20, value=5, step=1, key='max_points')

    # Filters below the map
    couvert = st.selectbox("🛖 Couvert", ["", "OUI", "NON"], key='couvert')
    acces = st.selectbox("🏛️Acces", ["", "clientele", "public", "privee"], key='acces')
    payant = st.selectbox("💵Payant", ["", "OUI", "NON"], key='payant')
    surveille = st.selectbox("👮Surveiller", ["", "OUI", "NON"], key='surveille')
    types = st.multiselect("❓Type", ["abri", "ancrage", "arceaux", "autres", "batiment", "casier", "inconnu", "ratelier"], default=[], key='types')

    if address:
        lat, lon = get_coordinates(address)
        # Call create_map with the user_location parameter
        st_map = create_map(lat, lon, df, radius=radius, max_points=int(max_points), user_location=(lat, lon))
        folium_static(st_map)

if __name__ == "__main__":
    main()


