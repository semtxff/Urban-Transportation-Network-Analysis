import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.directed_graph import G
from ToolBox.directed_graph import labels
from ToolBox.directed_graph import stops_df
from ToolBox.directed_graph import routes_df

# Add travel time if missing (assuming an average speed of 30 km/h)
if 'travel_time' not in routes_df.columns:
    average_speed_kmph = 30  # Average speed in km/h
    routes_df['travel_time'] = routes_df['distance'] / average_speed_kmph

# Add stops (nodes) and their positions
for _, row in stops_df.iterrows():
    G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))

# Add routes (edges) with distances and travel times as attributes
for _, row in routes_df.iterrows():
    G.add_edge(row['start_stop_id'], row['end_stop_id'], distance=row['distance'], travel_time=row['travel_time'])


# Calculate degree centrality
degree_centrality = nx.degree_centrality(G)

# Find the node with the highest centrality
max_centrality = max(degree_centrality.values())
most_central_node = [node for node, centrality in degree_centrality.items() if centrality == max_centrality]
print(f"中心度最高的站点是: {labels[most_central_node[0]]} (节点编号: {most_central_node[0]})")

# Function to calculate the efficiency of a path
def calculate_efficiency(path, graph):
    total_distance = 0
    total_travel_time = 0
    for i in range(len(path) - 1):
        edge_data = graph.get_edge_data(path[i], path[i+1])
        total_distance += edge_data['distance']
        total_travel_time += edge_data['travel_time']
    if total_travel_time == 0:
        return float('inf')  # Avoid division by zero
    return total_distance / total_travel_time

# Example: Finding the most efficient path between two nodes
start_node = 1  # Chatelet
end_node = 3    # Bastille

# Find the shortest path based on distance
shortest_path_distance = nx.dijkstra_path(G, start_node, end_node, weight='distance')
shortest_path_distance_efficiency = calculate_efficiency(shortest_path_distance, G)
print(f"Shortest path based on distance: {shortest_path_distance}")
print(f"Efficiency of shortest path: {shortest_path_distance_efficiency}")

# Find the shortest path based on travel time
shortest_path_time = nx.dijkstra_path(G, start_node, end_node, weight='travel_time')
shortest_path_time_efficiency = calculate_efficiency(shortest_path_time, G)
print(f"Shortest path based on travel time: {shortest_path_time}")
print(f"Efficiency of shortest path: {shortest_path_time_efficiency}")

# Check if the shortest path by distance is the most efficient
if shortest_path_distance_efficiency >= shortest_path_time_efficiency:
    print("The shortest path by distance is the most efficient.")
else:
    print("The shortest path by travel time is the most efficient.")