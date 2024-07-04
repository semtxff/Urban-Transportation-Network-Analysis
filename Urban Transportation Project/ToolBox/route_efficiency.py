import os
import sys
import heapq

# Get the directory of the current script file获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

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
    stop_times = {
        'Residential': 2,
        'Commercial': 4,
        'Industrial': 3,
        'Mixed': 3
    }
    
    average_speed = 40.0  # km/h
    travel_time = distance / average_speed * 60  # convert to minutes转换为分钟
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

# Task 2: Dijkstra algorithm to find the shortest path.Dijkstra算法来寻找最短路径
def dijkstra(graph, start, end):
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (distance, node)（距离，节点）
    
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    previous_nodes = {node: None for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        if current_node == end:
            path = []
            while previous_nodes[current_node] is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]
            path.insert(0, start)
            return path, current_distance
        
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return None, float('inf')

def create_weighted_graph(routes_df):
    graph = {}
    
    for _, row in routes_df.iterrows():
        start_stop_id = row['start_stop_id']
        end_stop_id = row['end_stop_id']
        distance = row['distance']
        
        if start_stop_id not in graph:
            graph[start_stop_id] = []
        graph[start_stop_id].append((end_stop_id, distance))
    
    return graph

# Task 3: Route efficiency analysis路线效率分析
def calculate_efficiency(total_distance, travel_time):
    return total_distance / travel_time if travel_time > 0 else float('inf')

def route_efficiency_analysis():
    from ToolBox.plt_graph import stops_df, routes_df
    from ToolBox.find_routes import start_node, end_node
    stops_graph = create_graph(stops_df, routes_df)
    weighted_graph = create_weighted_graph(routes_df)
    
    # Find all paths and calculate their travel times找到所有路径并计算其旅行时间
    all_paths = find_all_paths(stops_graph, start_node, end_node)
    paths_travel_times = calculate_paths_travel_time(stops_graph, all_paths)
    
    # Find the shortest path找到最短路径
    shortest_path, shortest_distance = dijkstra(weighted_graph, start_node, end_node)
    
    # Calculate the efficiency of each path计算每条路径的效率
    efficiencies = []
    for path, travel_time in paths_travel_times:
        total_distance = sum(stops_graph[path[i]]['edges'][path[i+1]] for i in range(len(path) - 1))
        efficiency = calculate_efficiency(total_distance, travel_time)
        efficiencies.append((path, efficiency, total_distance, travel_time))
    
    # Find the most efficient path找到最有效率的路径
    most_efficient_path = min(efficiencies, key=lambda x: x[1])
    
    print(f"Most efficient path: {' -> '.join(map(str, most_efficient_path[0]))}, Efficiency: {most_efficient_path[1]:.2f}, Total Distance: {most_efficient_path[2]:.2f} km, Travel Time: {most_efficient_path[3]:.2f} minutes")
    if shortest_path:
        print(f"The shortest path from {start_node} to {end_node} is: {' -> '.join(map(str, shortest_path))} with a total distance of {shortest_distance:.2f} km.")
    else:
        print(f"There is no path from {start_node} to {end_node}.")
    
    print(f"Is the shortest path the most efficient? {'Yes' if most_efficient_path[0] == shortest_path else 'No'}")