import pandas as pd
import folium

# Load data
data = pd.read_csv('urban_transport_network_stops.csv')

# Create map Objects
mymap = folium.Map(location=[data['latitude'].mean(), data['longitude'].mean()], zoom_start=12)

# Add stop to map
for index, row in data.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Stop ID: {row['stop_id']}<br>Name: {row['name']}<br>Zone Type: {row['zone_type']}"
    ).add_to(mymap)

# Save map
mymap.save('interactive_map.html')
