import os
import sys

# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

def create_graph(stops_df, routes_df):
    graph = {}
    
    for _, row in stops_df.iterrows():
        stop_id = row['stop_id']
        graph[stop_id] = {'pos': (row['longitude'], row['latitude']), 'name': row['name'], 'out_degree': 0, 'in_degree': 0}
    
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

def analyze_peak_hours_traffic(routes_df, congestion_factor=1.5, stop_delay=2):
    # Create a copy of the routes DataFrame to avoid modifying the original data创建路线 DataFrame 的副本以避免修改原始数据
    optimized_routes_df = routes_df.copy()
    
    # Calculate increased travel times due to congestion and stop delays计算因交通拥堵和站点延误而增加的行程时间
    optimized_routes_df['peak_hour_distance'] = optimized_routes_df['distance'] * congestion_factor
    optimized_routes_df['peak_hour_time'] = optimized_routes_df['peak_hour_distance'] / 10  # Assuming average speed is 10 km/h假设平均速度为 10 公里/小时
    optimized_routes_df['peak_hour_time'] += stop_delay  # Adding delay at each stop每站增加延误
    
    return optimized_routes_df

def dfs_find_all_paths(graph, start, end, path, all_paths):
    path.append(start)
    if start == end:
        all_paths.append(path.copy())
    else:
        for neighbor in graph.get(start, []):
            if neighbor not in path:
                dfs_find_all_paths(graph, neighbor, end, path, all_paths)
    path.pop()

def find_all_paths(graph, start, end):
    all_paths = []
    dfs_find_all_paths(graph, start, end, [], all_paths)
    return all_paths

def calculate_path_time(graph, path, optimized_routes_df):
    total_time = 0
    for i in range(len(path) - 1):
        start, end = path[i], path[i + 1]
        route = optimized_routes_df[(optimized_routes_df['start_stop_id'] == start) & (optimized_routes_df['end_stop_id'] == end)]
        if not route.empty:
            total_time += route.iloc[0]['peak_hour_time']
        else:
            return float('inf')  # If there are disconnected parts in the path, the path is considered invalid.如果路径中有不连通的部分，则认为此路径无效
    return total_time

def print_peak_hour_route_between_stops(graph, optimized_routes_df, start_stop_id, end_stop_id):
    all_paths = find_all_paths(graph, start_stop_id, end_stop_id)
    if not all_paths:
        print(f"No route found between stop {start_stop_id} and stop {end_stop_id}")
        return
    
    best_time = float('inf')
    best_path = None
    for path in all_paths:
        time = calculate_path_time(graph, path, optimized_routes_df)
        if time < best_time:
            best_time = time
            best_path = path

    if best_path:
        path_str = " -> ".join(map(str, best_path))
        print(f"Best route from {start_stop_id} to {end_stop_id} during peak hours: {path_str} with total time {best_time:.2f} minutes")
    else:
        print(f"No valid route found between stop {start_stop_id} and stop {end_stop_id}")