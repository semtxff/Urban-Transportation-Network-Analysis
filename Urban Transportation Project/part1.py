from enum import Enum, auto
import pandas as pd
import itertools

class ZoneType(Enum):
    RESIDENTIAL = auto()
    COMMERCIAL = auto()
    INDUSTRIAL = auto()
    MIXED = auto()

class TransportStop:
    def __init__(self, stop_id, name, latitude, longitude, zone_type):
        self.stop_id = stop_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        if isinstance(zone_type, ZoneType):
            self.zone_type = zone_type
        else:
            raise ValueError("Invalid zone_type value")

    def __str__(self):
        return f"Stop {self.stop_id}: {self.name} ({self.latitude}, {self.longitude}), Zone: {self.zone_type.name}"

    def __repr__(self):
        return f"TransportStop(stop_id={self.stop_id}, name='{self.name}', latitude={self.latitude}, longitude={self.longitude}, zone_type={self.zone_type})"

    def __lt__(self, other):
        return self.stop_id < other.stop_id

# Read data from a CSV file
def read_stops_from_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        stops = []
        for _, row in data.iterrows():
            stop = TransportStop(
                stop_id=row['stop_id'],
                name=row['name'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                zone_type=ZoneType[row['zone_type'].upper()]  # Convert to uppercase and match enum value
            )
            stops.append(stop)
        return stops
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

# File path
csv_file_path = "urban_transport_network_stops.csv"
transport_stops = read_stops_from_csv(csv_file_path)

# Compare stops
for stop_pair in itertools.combinations(transport_stops, 2):
    stop_a, stop_b = stop_pair


import networkx as nx
import matplotlib.pyplot as plt

node_labels={1:"Chatelet",2:"Gare de Lyon",3:"Bastille",4:"Nation",5:"Opera",6:"Republique",7:"Montparnasse",8:"La Defense",9:"Saint-Lazare"}

# Read latitude and longitude data from a CSV file
stops_df = pd.read_csv("urban_transport_network_stops.csv")

# Read distance data from a CSV file
routes_df = pd.read_csv("urban_transport_network_routes.csv")

# Create a directed graph
G = nx.DiGraph()

# Add sites and edges
for _, row in stops_df.iterrows():
    G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))

for _, row in routes_df.iterrows():
    G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])

labels = {node: node_labels.get(node, node) for node in G.nodes()}

# Draw a directed graph
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, labels=labels, node_size=100, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrows=True)
plt.title("Transport Network Directed Graph")
plt.show()