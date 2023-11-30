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
    st.sidebar.title("Où garer mon Velo - Controls")

    # Sidebar controls
    address = st.sidebar.text_input("Entrer une adresse en Île-de-France", key='address')
    radius = st.sidebar.slider("Rayon en Km (max 5km)", min_value=0.5, max_value=5.0, value=1.0, step=0.1, key='radius')
    max_points = st.sidebar.number_input("Nombre d'abri à afficher (max 20)", min_value=1, max_value=20, value=5, step=1, key='max_points')

    couvert = st.sidebar.selectbox("Couvert?", ["", "OUI", "NON"], key='couvert')
    acces = st.sidebar.selectbox("Acces?", ["", "clientele", "public", "privee"], key='acces')
    payant = st.sidebar.selectbox("Payant?", ["", "OUI", "NON"], key='payant')
    surveille = st.sidebar.selectbox("Surveiller?", ["", "OUI", "NON"], key='surveille')
    types = st.sidebar.multiselect("Type?", ["abri", "ancrage", "arceaux", "autres", "batiment", "casier", "inconnu", "ratelier"], default=[], key='types')

    # Main page content
    st.title("Où garer mon Velo - Map")
    if address:
        lat, lon = get_coordinates(address)
        st_map = create_map(lat, lon, df, radius=radius, max_points=int(max_points))
        folium_static(st_map)

    # Sidebar - Additional Information
    st.sidebar.info("About the App: This app helps you find bicycle parking locations in Île-de-France.")
    st.sidebar.text("Instructions: Enter an address, adjust the search radius and number of points, and apply filters as needed.")

    # Optional: Sidebar - Contact or Feedback
    st.sidebar.text("Contact: Your Contact Info")
    feedback = st.sidebar.text_area("Feedback: Leave your comments here!")

if __name__ == "__main__":
    main()

