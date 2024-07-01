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
    max_total_degree = -1
    max_total_node = None
    
    for node, attributes in graph.items():
        total_degree = attributes['out_degree'] + attributes['in_degree']
        if total_degree > max_total_degree:
            max_total_degree = total_degree
            max_total_node = node
    
    return max_total_node, max_total_degree


# 找到中心度最高的车站
max_total_node, max_total_degree = find_highest_centrality(G)

# 输出结果
if max_total_node is not None:
    print(f"The station with the highest total degree (sum of out-degree and in-degree) is {G[max_total_node]['name']} ({max_total_node}) with {max_total_degree} connections.")
else:
    print("No node with connections found.")

# 绘制图形
plot_transport_network(G)

