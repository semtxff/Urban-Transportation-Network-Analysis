import networkx as nx

# Add travel time if missing (assuming an average speed of 30 km/h)
def create_and_configure_graph(stops_df,routes_df):
    if 'travel_time' not in routes_df.columns:
        average_speed_kmph = 30  # Average speed in km/h
        routes_df['travel_time'] = routes_df['distance'] / average_speed_kmph
    # Add stops (nodes) and their positions
    for _, row in stops_df.iterrows():
        G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))
    # Add routes (edges) with distances and travel times as attributes
    for _, row in routes_df.iterrows():
        G.add_edge(row['start_stop_id'], row['end_stop_id'], distance=row['distance'], travel_time=row['travel_time'])

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
    calculate_result = '{:.2f}'.format(total_distance / total_travel_time)
    return calculate_result

# Find the shortest path based on distance
def shortest_path():
    shortest_path_distance = nx.dijkstra_path(G, start_node, end_node, weight='distance')
    shortest_path_distance_efficiency = calculate_efficiency(shortest_path_distance, G)
    print(f"Shortest path based on distance: {shortest_path_distance}")
    print(f"Efficiency of shortest path: {shortest_path_distance_efficiency}")

    shortest_path_time = nx.dijkstra_path(G, start_node, end_node, weight='travel_time')
    shortest_path_time_efficiency = calculate_efficiency(shortest_path_time, G)
    print(f"Shortest path based on travel time: {shortest_path_time}")
    print(f"Efficiency of shortest path: {shortest_path_time_efficiency}")

    if shortest_path_distance_efficiency >= shortest_path_time_efficiency:
        print("The shortest path by distance is the most efficient.")
    else:
        print("The shortest path by travel time is the most efficient.")

# 在其他代码中调用
G = nx.DiGraph()
print()
start_node = int(input("Please set start node:"))
end_node = int(input("Please set end node:"))