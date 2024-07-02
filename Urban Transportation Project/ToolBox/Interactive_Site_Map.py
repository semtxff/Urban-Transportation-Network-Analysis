import pandas as pd
import folium

# Load data
stops_df = pd.read_csv("urban_transport_network_stops.csv")
routes_df = pd.read_csv("urban_transport_network_routes.csv")

# Create a map centered at an average location
m = folium.Map(location=[stops_df['latitude'].mean(), stops_df['longitude'].mean()], zoom_start=13)

# Add stops to the map
for _, row in stops_df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Name: {row['name']}<br>Zone: {row['zone_type']}",
        tooltip=row['name']
    ).add_to(m)

# Save the map to an HTML file
m.save("interactive_transport_network_map.html")

