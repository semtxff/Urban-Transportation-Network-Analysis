import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

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