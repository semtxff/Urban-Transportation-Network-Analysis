import os
import sys
# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.directed_graph import G

def dijkstra(graph, start_node, end_node):
    # 初始化距离字典，将起点到各个节点的距离设为无穷大
    distances = {node: float('inf') for node in graph.nodes()}
    distances[start_node] = 0

    # 初始化前驱节点字典
    previous_nodes = {node: None for node in graph.nodes()}

    # 初始化已访问节点集合
    visited = set()

    while len(visited) < len(graph.nodes()):
        # 选择距离最小的未访问节点
        current_node = min((node for node in graph.nodes() if node not in visited), key=distances.get)
        visited.add(current_node)

        # 更新邻接节点的距离
        for neighbor, data in graph[current_node].items():
            weight = data['weight']
            new_distance = distances[current_node] + weight
            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                previous_nodes[neighbor] = current_node

    # 构建最短路径
    path = []
    current = end_node
    while current is not None:
        path.append(current)
        current = previous_nodes[current]
    path.reverse()

    return path, distances[end_node]

def print_shortest_path():
    start_node = int(input("Please set start node:"))
    end_node = int(input("Please set end node:"))
    shortest_path, shortest_distance = dijkstra(G, start_node, end_node)
    print(f"最短路径为：{shortest_path}，总距离为：{shortest_distance:.2f} km")