import os
import sys
import matplotlib.pyplot as plt
# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import G
from ToolBox.plt_graph import plot_transport_network

def find_highest_centrality(graph):
    max_out_degree = -1
    max_in_degree = -1
    max_out_node = None
    max_in_node = None
    
    for node, attributes in graph.items():
        if 'out_degree' in attributes and attributes['out_degree'] > max_out_degree:
            max_out_degree = attributes['out_degree']
            max_out_node = node
        if 'in_degree' in attributes and attributes['in_degree'] > max_in_degree:
            max_in_degree = attributes['in_degree']
            max_in_node = node
    
    return max_out_node, max_out_degree, max_in_node, max_in_degree


# 找到中心度最高的车站
max_out_node, max_out_degree, max_in_node, max_in_degree = find_highest_centrality(G)

# 输出结果
if max_out_node is not None:
    print(f"The station with the highest out-degree (most outgoing connections) is {G[max_out_node]['name']} ({max_out_node}) with {max_out_degree} connections.")
else:
    print("No node with outgoing connections found.")

if max_in_node is not None:
    print(f"The station with the highest in-degree (most incoming connections) is {G[max_in_node]['name']} ({max_in_node}) with {max_in_degree} connections.")
else:
    print("No node with incoming connections found.")

# 绘制图形
plot_transport_network(G)

