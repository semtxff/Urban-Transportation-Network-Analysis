import os
import sys

# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import stops_df, routes_df

def create_graph(stops_df, routes_df):
    graph = {}
    
    for _, row in stops_df.iterrows():
        stop_id = row['stop_id']
        graph[stop_id] = {'pos': (row['longitude'], row['latitude']), 'name': row['name'], 'zone_type': row['zone_type'], 'out_degree': 0, 'in_degree': 0}
    
    for _, row in routes_df.iterrows():
        start_stop_id = row['start_stop_id']
        end_stop_id = row['end_stop_id']
        distance = row['distance']
        
        if start_stop_id not in graph:
            graph[start_stop_id] = {'pos': (0, 0), 'name': '', 'zone_type': '', 'out_degree': 0, 'in_degree': 0}
        if end_stop_id not in graph:
            graph[end_stop_id] = {'pos': (0, 0), 'name': '', 'zone_type': '', 'out_degree': 0, 'in_degree': 0}
        
        if 'edges' not in graph[start_stop_id]:
            graph[start_stop_id]['edges'] = {}
        graph[start_stop_id]['edges'][end_stop_id] = distance
        graph[start_stop_id]['out_degree'] += 1
        graph[end_stop_id]['in_degree'] += 1
    
    return graph

def calculate_travel_time(distance, start_zone, end_zone):
    # Define stop times based on zone_type
    stop_times = {
        'Residential': 2,
        'Commercial': 4,
        'Industrial': 3,
        'Mixed': 3
    }
    
    average_speed = 40.0  # km/h
    travel_time = distance / average_speed * 60  # convert to minutes
    start_stop_time = stop_times.get(start_zone, 0)
    end_stop_time = stop_times.get(end_zone, 0)
    
    return travel_time + start_stop_time + end_stop_time

def find_all_paths(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in graph:
        return []
    paths = []
    for node in graph[start].get('edges', {}):
        if node not in path:
            new_paths = find_all_paths(graph, node, end, path)
            for p in new_paths:
                paths.append(p)
    return paths

def calculate_paths_travel_time(graph, paths):
    paths_travel_time = []
    for path in paths:
        total_travel_time = 0
        for i in range(len(path) - 1):
            start = path[i]
            end = path[i + 1]
            distance = graph[start]['edges'][end]
            start_zone = graph[start]['zone_type']
            end_zone = graph[end]['zone_type']
            travel_time = calculate_travel_time(distance, start_zone, end_zone)
            total_travel_time += travel_time
        paths_travel_time.append((path, total_travel_time))
    return paths_travel_time


def print_time_predict():
    # Find all paths and calculate their travel times
    from ToolBox.find_routes import start_node, end_node
    G = create_graph(stops_df, routes_df)
    all_paths = find_all_paths(G, start_node, end_node)
    paths_travel_times = calculate_paths_travel_time(G, all_paths)
    for path, travel_time in paths_travel_times:
        print(f"Path: {' -> '.join(map(str, path))}, Travel time: {travel_time:.2f} minutes")
