import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import os
import sys

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from directed_graph import G
from directed_graph import node_labels
from directed_graph import labels
from directed_graph import pos
from directed_graph import stops_df
from directed_graph import routes_df

for _, row in stops_df.iterrows():
    G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))

for _, row in routes_df.iterrows():
    G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])

# 找到所有从Chatelet到Bastille的路径
def find_paths(G, start, end, path=[]):
    path = path + [start]
    if start == end:
        return [path]
    if start not in G:
        return []
    paths = []
    for node, _ in G[start]:  # 只取节点，不考虑权重
        if node not in path:
            new_paths = find_paths(G, node, end, path)
            for new_path in new_paths:
                paths.append(new_path)
    return paths

# 将Graph转换为字典表示，以便于路径搜索
G_dict = {node: [] for node in G.nodes()}
for start, end, data in G.edges(data=True):
    G_dict[start].append((end, data.get('weight', 1)))

# 查找所有路径
start_node = node_labels[1]  # Chatelet
end_node = node_labels[3]    # Bastille
all_paths = find_paths(G_dict, start_node, end_node)

# 输出所有路径
for i, path in enumerate(all_paths):
    print(f"路径 {i+1}: {path}")

# 绘制图
nx.draw(G, pos, with_labels=True, labels=labels, node_size=100, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrows=True)
plt.title("Transport Network Directed Graph")
plt.show()