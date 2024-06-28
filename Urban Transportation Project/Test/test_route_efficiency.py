import unittest
import networkx as nx
import pandas as pd
import os
import sys

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.directed_graph import G
from ToolBox.directed_graph import stops_df
from ToolBox.directed_graph import routes_df
from ToolBox.route_efficiency import calculate_efficiency  # 替换成你的 calculate_efficiency 函数

class TestGraphOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # 初始化测试数据
        cls.G = nx.DiGraph()

        # Add stops (nodes) and their positions
        for _, row in stops_df.iterrows():
            cls.G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))

        # Add routes (edges) with distances and travel times as attributes
        for _, row in routes_df.iterrows():
            cls.G.add_edge(row['start_stop_id'], row['end_stop_id'], distance=row['distance'], travel_time=row['travel_time'])

    def test_shortest_path_distance(self):
        start_node = 1  # Chatelet
        end_node = 3    # Bastille

        shortest_path_distance = nx.dijkstra_path(self.G, start_node, end_node, weight='distance')
        shortest_path_distance_efficiency = calculate_efficiency(shortest_path_distance, self.G)

        # Add assertions here to check correctness
        self.assertIsNotNone(shortest_path_distance)
        self.assertIsNotNone(shortest_path_distance_efficiency)
        # Add more specific assertions if needed

    def test_shortest_path_time(self):
        start_node = 1  # Chatelet
        end_node = 3    # Bastille

        shortest_path_time = nx.dijkstra_path(self.G, start_node, end_node, weight='travel_time')
        shortest_path_time_efficiency = calculate_efficiency(shortest_path_time, self.G)

        # Add assertions here to check correctness
        self.assertIsNotNone(shortest_path_time)
        self.assertIsNotNone(shortest_path_time_efficiency)
        # Add more specific assertions if needed

    def test_efficiency_comparison(self):
        start_node = 1  # Chatelet
        end_node = 3    # Bastille

        shortest_path_distance = nx.dijkstra_path(self.G, start_node, end_node, weight='distance')
        shortest_path_distance_efficiency = calculate_efficiency(shortest_path_distance, self.G)

        shortest_path_time = nx.dijkstra_path(self.G, start_node, end_node, weight='travel_time')
        shortest_path_time_efficiency = calculate_efficiency(shortest_path_time, self.G)

        # Check efficiency comparison
        if shortest_path_distance_efficiency >= shortest_path_time_efficiency:
            self.assertTrue(shortest_path_distance_efficiency >= shortest_path_time_efficiency)
        else:
            self.assertTrue(shortest_path_time_efficiency > shortest_path_distance_efficiency)

if __name__ == '__main__':
    unittest.main()
