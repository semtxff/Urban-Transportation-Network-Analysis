import pandas as pd
import matplotlib.pyplot as plt

def load_stops_df(filename):
    # Read site data读取站点数据
    stops_df = pd.read_csv(filename)
    return stops_df

def load_routes_df(filename):
    # Read route data读取路线数据
    routes_df = pd.read_csv(filename)
    return routes_df

def create_graph(stops_df, routes_df):
    # Create an empty directed graph创建空的有向图
    graph = {}
    
    # Add a site添加站点
    for _, row in stops_df.iterrows():
        stop_id = row['stop_id']
        graph[stop_id] = {'pos': (row['longitude'], row['latitude']), 'name': row['name'], 'out_degree': 0, 'in_degree': 0}
    
    # Add Edge添加边
    for _, row in routes_df.iterrows():
        start_stop_id = row['start_stop_id']
        end_stop_id = row['end_stop_id']
        distance = row['distance']
        
        if start_stop_id not in graph:
            graph[start_stop_id] = {'pos': (0, 0), 'name': '', 'out_degree': 0, 'in_degree': 0}
        if end_stop_id not in graph:
            graph[end_stop_id] = {'pos': (0, 0), 'name': '', 'out_degree': 0, 'in_degree': 0}
        
        graph[start_stop_id][end_stop_id] = distance
        graph[start_stop_id]['out_degree'] += 1
        graph[end_stop_id]['in_degree'] += 1
    
    return graph

def plot_transport_network(graph):
    plt.figure(figsize=(10, 8))
    for node, neighbors in graph.items():
        x, y = neighbors['pos']
        plt.scatter(x, y, s=100, label=f"{neighbors['name']} ({node})")
        for neighbor, distance in neighbors.items():
            if neighbor not in {'pos', 'name', 'out_degree', 'in_degree'}:
                x_neighbor, y_neighbor = graph[neighbor]['pos']
                dx, dy = x_neighbor - x, y_neighbor - y
                plt.arrow(x, y, dx, dy, head_width=0.003, head_length=0.01, fc='gray', ec='gray', alpha=0.5)
                plt.text((x + x_neighbor) / 2, (y + y_neighbor) / 2, f"{distance:.1f}", fontsize=8)

    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title("Urban Transport Network")
    plt.legend()
    plt.grid(True)
    plt.show()
# Download Data加载数据
stops_df = load_stops_df("urban_transport_network_stops.csv")
routes_df = load_routes_df("urban_transport_network_routes.csv")

# Creating a directed graph创建有向图
G = create_graph(stops_df, routes_df)