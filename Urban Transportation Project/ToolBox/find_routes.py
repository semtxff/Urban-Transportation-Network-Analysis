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

# 查找所有从Chatelet到Bastille的简单路径
start_node = 1  # Chatelet 的节点 ID
end_node = 3    # Bastille 的节点 ID
all_paths = list(nx.all_simple_paths(G, source=start_node, target=end_node))

# 输出路径信息
print(f"从Chatelet到Bastille的所有路径信息：")
for i, path in enumerate(all_paths, 1):
    path_labels = [node_labels[node] for node in path]
    print(f"路径 {i}: {' -> '.join(path_labels)}")