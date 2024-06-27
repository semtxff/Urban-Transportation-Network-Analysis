import unittest
import networkx as nx
import pandas as pd

class TestUrbanTransportNetwork(unittest.TestCase):
    
    def setUp(self):
        # 设置测试前的准备工作
        self.stops_df = pd.read_csv("urban_transport_network_stops.csv")
        self.routes_df = pd.read_csv("urban_transport_network_routes.csv")
        self.G = nx.DiGraph()
        
        for _, row in self.stops_df.iterrows():
            self.G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))
        
        for _, row in self.routes_df.iterrows():
            self.G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])
    
    def test_shortest_path_distance(self):
        # 测试最短路径距离计算
        shortest_paths = nx.single_source_dijkstra_path_length(self.G, source=1, weight='weight')
        self.assertEqual(shortest_paths[2], 10.5)  # 例如，检查从Chatelet到Gare de Lyon的距离是否为5公里
    
    def test_shortest_path_nodes(self):
        # 测试最短路径节点计算
        shortest_paths = nx.single_source_dijkstra_path(self.G, source=1, weight='weight')
        self.assertEqual(shortest_paths[2], [1, 2])  # 检查从Chatelet到Gare de Lyon的节点路径是否正确
    
    # 可以添加更多的测试方法，以检查其他功能和边界情况

if __name__ == '__main__':
    unittest.main()

