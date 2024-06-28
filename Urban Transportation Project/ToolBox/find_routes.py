import networkx as nx
import os
import sys

# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path(将上级目录（项目根目录）添加到系统路径中)
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from directed_graph import node_labels
from directed_graph import G

# Find all routes from Chatelet to Bastille(查找所有从Chatelet到Bastille的路径)
start_node = 1  # Chatelet ID
end_node = 3    # Bastille ID
all_paths = list(nx.all_simple_paths(G, source=start_node, target=end_node))

# output输出路径信息
print(f"All path information from Chatelet to Bastille：")
for i, path in enumerate(all_paths, 1):
    path_labels = [node_labels[node] for node in path]
    print(f"Path {i}: {' -> '.join(path_labels)}")