import os
import sys

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import stops_df
from ToolBox.plt_graph import G

# 估计停车时间
zone_type_times = {
    'Residential': 2,
    'Commercial': 4,
    'Industrial': 3,
    'Mixed': 3
}

def estimate_travel_time(route):
    total_time = 0
    for stop_id in route:
        zone_type = stops_df.loc[stops_df['stop_id'] == stop_id, 'zone_type'].values[0]
        total_time += zone_type_times.get(zone_type, 0)
    return total_time

# 计算最短路径
def shortest_path(source, target):
    visited = set()
    distances = {stop_id: float('inf') for stop_id in G}
    distances[source] = 0
    prev = {}

    while len(visited) < len(G):
        current = min((stop_id for stop_id in G if stop_id not in visited), key=distances.get)
        visited.add(current)

        for neighbor, edge_info in G[current].items():
            if isinstance(edge_info, (int, float)):
                distance = edge_info
            elif isinstance(edge_info, dict) and 'distance' in edge_info:
                distance = edge_info['distance']
            else:
                continue  # 跳过非边信息

            if neighbor not in visited:
                new_distance = distances[current] + distance
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    prev[neighbor] = current

    path = []
    node = target
    while node != source:
        path.append(node)
        node = prev.get(node, source)
    path.append(source)
    path.reverse()

    travel_time = estimate_travel_time(path)
    print(f"Shortest path from {source} to {target}: {path}")
    print(f"Estimated travel time: {travel_time} minutes")

# 示例：计算从1到6的最短路径
shortest_path(1, 6)