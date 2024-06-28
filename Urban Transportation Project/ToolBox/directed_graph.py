import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

node_labels={1:"Chatelet",2:"Gare de Lyon",3:"Bastille",4:"Nation",5:"Opera",6:"Republique",7:"Montparnasse",8:"La Defense",9:"Saint-Lazare"}

# Read latitude and longitude data from a CSV file（从 CSV 文件读取纬度和经度数据）
stops_df = pd.read_csv("urban_transport_network_stops.csv")

# Read distance data from a CSV file（从 CSV 文件读取距离数据）
routes_df = pd.read_csv("urban_transport_network_routes.csv")

# Create a directed graph（创建有向图）
G = nx.DiGraph()

# Add sites and edges（添加站点和边缘）
for _, row in stops_df.iterrows():
    G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))

for _, row in routes_df.iterrows():
    G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])

labels = {node: node_labels.get(node, node) for node in G.nodes()}

# Draw a directed graph（绘制有向图）
pos = nx.get_node_attributes(G, 'pos')
nx.draw(G, pos, with_labels=True, labels=labels, node_size=100, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrows=True)
plt.title("Transport Network Directed Graph")
plt.show()

# Calculate the degree centrality of each node（计算每个节点的度中心性）
degree_centrality = nx.degree_centrality(G)

# Find the site with the highest centrality（找出中心度最高的站点）
max_centrality = max(degree_centrality.values())
most_central_node = [node for node, centrality in degree_centrality.items() if centrality == max_centrality]
print(f"中心度最高的站点是: {labels[most_central_node[0]]} (节点编号: {most_central_node[0]})")