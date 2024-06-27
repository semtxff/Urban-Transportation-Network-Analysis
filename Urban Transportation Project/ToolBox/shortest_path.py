import csv
from collections import defaultdict

def read_csv(filename):
    data = defaultdict(dict)
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_stop = int(row.get('start', 0))  # Use .get() to handle missing keys
            end_stop = int(row.get('end', 0))
            distance = float(row.get('dist', 0))
            data[start_stop][end_stop] = distance
            data[end_stop][start_stop] = distance  # Add the reverse edge for an undirected graph
    return data

def dijkstra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    visited = set()

    while len(visited) < len(graph):
        current_node = min((node for node in graph if node not in visited), key=distances.get)
        visited.add(current_node)

        for neighbor, weight in graph[current_node].items():
            if distances[current_node] + weight < distances[neighbor]:
                distances[neighbor] = distances[current_node] + weight

    return distances

if __name__ == '__main__':
    stops_graph = read_csv('urban_transport_network_stops.csv')
    start_node = 1  # Assume the starting point is stop 1
    shortest_distances = dijkstra(stops_graph, start_node)

    # Print the shortest distances
    for end_node, distance in shortest_distances.items():
        print(f"从站点 {start_node} 到站点 {end_node} 的最短距离为 {distance:.2f} 单位（如米或千米）。")
