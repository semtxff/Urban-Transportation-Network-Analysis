import networkx as nx

def find_all_paths(G, start_node, end_node):
    # 查找所有从start_node到end_node的路径
    all_paths = list(nx.all_simple_paths(G, source=start_node, target=end_node))
    return all_paths

def print_paths(all_paths, node_labels):
    # 输出路径信息
    print(f"All path information from Chatelet to Bastille：")
    for i, path in enumerate(all_paths, 1):
        path_labels = [node_labels[node] for node in path]
        print(f"Path {i}: {' -> '.join(path_labels)}")

# 在其他代码中调用
start_node = 1
end_node = 3