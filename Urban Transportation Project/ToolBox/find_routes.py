import os
import sys
# Get the directory of the current script file获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import routes_df
from tkinter import simpledialog

def dfs(graph, start, end, visited, path):
    visited[start] = True
    path.append(start)

    if start == end:
        print("Route:", path)
    else:
        for neighbor in graph.get(start, []):
            if not visited[neighbor]:
                dfs(graph, neighbor, end, visited, path)

    path.pop()
    visited[start] = False

# Creating a directed graph创建有向图
def create_graph():   
    graph = {}

    for _, row in routes_df.iterrows():
        start_stop_id = row['start_stop_id']
        end_stop_id = row['end_stop_id']

        if start_stop_id not in graph:
            graph[start_stop_id] = []
        graph[start_stop_id].append(end_stop_id)

    # Initialize access tokens and paths初始化访问标记和路径
    visited = {node: False for node in graph}
    path = []

    # Find all possible routes查找所有可能的路线 
    dfs(graph, start_node, end_node, visited, path)

start_node = int(simpledialog.askstring("Type", "start node:"))
end_node = int(simpledialog.askstring("Type", "end node:"))