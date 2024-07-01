import pandas as pd
import matplotlib.pyplot as plt

def load_stops_df(filename):
    # Read stop data
    stops_df = pd.read_csv(filename)
    return stops_df

def load_routes_df(filename):
    # Read route data
    routes_df = pd.read_csv(filename)
    return routes_df

def create_graph(stops_df, routes_df):
    # Create an empty directed graph
    graph = {}
    
    # Add stops
    for _, row in stops_df.iterrows():
        stop_id = row['stop_id']
        graph[stop_id] = {'pos': (row['longitude'], row['latitude']), 'name': row['name']}
    
    # Add edges
    for _, row in routes_df.iterrows():
        start_stop_id = row['start_stop_id']
        end_stop_id = row['end_stop_id']
        distance = row['distance']
        
        if start_stop_id not in graph:
            graph[start_stop_id] = {}
        if end_stop_id not in graph:
            graph[end_stop_id] = {}
        
        graph[start_stop_id][end_stop_id] = distance
    
    return graph

def plot_transport_network(graph):
    plt.figure(figsize=(10, 8))
    for node, neighbors in graph.items():
        x, y = neighbors['pos']
        plt.scatter(x, y, s=100, label=f"{neighbors['name']} ({node})")
        for neighbor, distance in neighbors.items():
            if neighbor != 'pos' and neighbor != 'name':
                x_neighbor, y_neighbor = graph[neighbor]['pos']
                plt.plot([x, x_neighbor], [y, y_neighbor], linestyle='--', color='gray', alpha=0.5)
                plt.text((x + x_neighbor) / 2, (y + y_neighbor) / 2, f"{distance:.1f}", fontsize=8)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Urban Transport Network")
    plt.legend()
    plt.grid(True)
    plt.show()

# Load data
stops_df = load_stops_df("urban_transport_network_stops.csv")
routes_df = load_routes_df("urban_transport_network_routes.csv")

# Create the directed graph
my_graph = create_graph(stops_df, routes_df)

# Plot the graph
plot_transport_network(my_graph)
