import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

def load_stops_df():
    # 读取站点数据
    stops_df = pd.read_csv("urban_transport_network_stops.csv")
    return stops_df

def load_routes_df():
    # 读取路线数据
    routes_df = pd.read_csv("urban_transport_network_routes.csv")
    return routes_df

def create_graph(stops_df, routes_df):
    # 创建有向图
    G = nx.DiGraph()
    # 添加站点
    for _, row in stops_df.iterrows():
        G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))
    # 添加边
    for _, row in routes_df.iterrows():
        G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])
    return G

def node_label():
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
    return node_labels

def draw_graph(G, labels):
    # 绘制有向图
    pos = nx.get_node_attributes(G, 'pos')
    nx.draw(G, pos, with_labels=True, labels=labels, node_size=100, node_color="skyblue", font_size=10, font_color="black", font_weight="bold", arrows=True)
    plt.title("Transport Network Directed Graph")
    plt.show()

def calculate_degree_centrality(G):
    # 计算度中心性
    degree_centrality = nx.degree_centrality(G)
    return degree_centrality

def find_most_central_node(G, labels):
    degree_centrality = calculate_degree_centrality(G)
    # 找出中心度最高的站点
    max_centrality = max(degree_centrality.values())
    most_central_node = [node for node, centrality in degree_centrality.items() if centrality == max_centrality]
    print(f"中心度最高的站点是: {labels[most_central_node[0]]} (节点编号：{most_central_node[0]})")

# 在其他代码中调用
stops_df = load_stops_df()
routes_df = load_routes_df()
G = create_graph(stops_df, routes_df)
labels = node_label()