import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

node_labels = {
    1: "Chatelet",
    2: "Gare de Lyon",
    3: "Bastille",
    4: "Nation",
    5: "Opera",
    6: "Republique",
    7: "Montparnasse",
    8: "La Defense",
    9: "Saint-Lazare"
}

# 读取站点数据
stops_df = pd.read_csv("urban_transport_network_stops.csv")

# 读取路线数据
routes_df = pd.read_csv("urban_transport_network_routes.csv")

# 创建有向图
G = nx.DiGraph()

# 添加站点和边
for _, row in stops_df.iterrows():
    G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))

for _, row in routes_df.iterrows():
    G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])

# 计算最短路径
shortest_paths = nx.single_source_dijkstra_path_length(G, source=1, weight='weight')

# 打印从起点站到其他站点的最短路径
for target, distance in shortest_paths.items():
    print(f"从Chatelet (1) 到 {node_labels.get(target, target)} 的最短路径：{distance:.2f} 公里")

# 获取从 Chatelet (1) 到每个节点的最短路径
for target, path in nx.single_source_dijkstra_path(G, source=1, weight='weight').items():
    print(f"从 Chatelet 到 {node_labels.get(target, target)} 的最短路径节点：", path)


# 绘制有向图
labels = {node: node_labels.get(node, node) for node in G.nodes()}
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, labels=labels, node_size=100, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrows=True)
plt.title("交通网络有向图")
plt.show()
