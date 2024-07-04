import os
import sys
import heapq

# Get the directory of the current script file获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import routes_df

def dijkstra(graph, start, end):
    # Creating a priority queue创建一个优先级队列
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (distance, node)
    
    # Create a dictionary to store the shortest distance from the starting point to each node创建一个字典以存储从起点到每个节点的最短距离
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Create a dictionary to store predecessor nodes so that the path can be reconstructed创建一个字典以存储前驱节点，以便重构路径
    previous_nodes = {node: None for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # If the current node is the end point, build and return the path如果当前节点就是终点，构建并返回路径
        if current_node == end:
            path = []
            while previous_nodes[current_node] is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]
            path.insert(0, start)
            return path, current_distance
        
        # Traverse the neighbors of the current node遍历当前节点的邻居
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            # If a shorter path is found, update the distance and predecessor node, and add the neighbor to the queue如果找到更短的路径，更新距离和前驱节点，并将邻居加入队列
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return None, float('inf')

# Creating a directed weighted graph创建有向带权图
def create_graph():
    graph = {}
    
    for _, row in routes_df.iterrows():
        start_stop_id = row['start_stop_id']
        end_stop_id = row['end_stop_id']
        distance = row['distance']
        
        if start_stop_id not in graph:
            graph[start_stop_id] = []
        graph[start_stop_id].append((end_stop_id, distance))
    
    return graph

def print_shortest_path():
    from ToolBox.find_routes import start_node, end_node
    graph = create_graph()
    shortest_path, total_distance = dijkstra(graph, start_node, end_node)
    if shortest_path:
        print(f"The shortest path from {start_node} to {end_node} is: {shortest_path} with a total distance of {total_distance}.")
    else:
        print(f"There is no path from {start_node} to {end_node}.")