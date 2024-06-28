import networkx as nx
import os
import sys

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from directed_graph import node_labels
from directed_graph import G

# 计算最短路径
shortest_paths = nx.single_source_dijkstra_path_length(G, source=1, weight='weight')
# 打印从起点站到其他站点的最短路径
for target, distance in shortest_paths.items():
    print(f"从Chatelet (1) 到 {node_labels.get(target, target)} 的最短路径：{distance:.2f} 公里")

# 获取从 Chatelet (1) 到每个节点的最短路径
for target, path in nx.single_source_dijkstra_path(G, source=1, weight='weight').items():
    print(f"从 Chatelet 到 {node_labels.get(target, target)} 的最短路径节点：", path)