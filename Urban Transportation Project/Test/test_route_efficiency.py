import unittest
import pandas as pd
import os
import sys

# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
from ToolBox.route_efficiency import create_graph, calculate_travel_time, find_all_paths, calculate_paths_travel_time, dijkstra, create_weighted_graph, calculate_efficiency

class TestTransportNetwork(unittest.TestCase):

    def setUp(self):
        # 创建测试数据
        self.stops_df = pd.DataFrame({
            'stop_id': [1, 2, 3, 4],
            'name': ['A', 'B', 'C', 'D'],
            'longitude': [0.0, 1.0, 2.0, 3.0],
            'latitude': [0.0, 1.0, 2.0, 3.0],
            'zone_type': ['Residential', 'Commercial', 'Industrial', 'Mixed']
        })
        
        self.routes_df = pd.DataFrame({
            'start_stop_id': [1, 1, 2, 3],
            'end_stop_id': [2, 3, 3, 4],
            'distance': [1.0, 2.0, 1.0, 1.0]
        })

    def test_create_graph(self):
        graph = create_graph(self.stops_df, self.routes_df)
        self.assertEqual(len(graph), 4)
        self.assertIn('edges', graph[1])
        self.assertEqual(graph[1]['edges'][2], 1.0)
        self.assertEqual(graph[1]['edges'][3], 2.0)
        self.assertEqual(graph[2]['edges'][3], 1.0)
        self.assertEqual(graph[3]['edges'][4], 1.0)

    def test_calculate_travel_time(self):
        travel_time = calculate_travel_time(10, 'Residential', 'Commercial')
        expected_time = 10 / 40 * 60 + 2 + 4
        self.assertAlmostEqual(travel_time, expected_time)

    def test_find_all_paths(self):
        graph = create_graph(self.stops_df, self.routes_df)
        paths = find_all_paths(graph, 1, 4)
        expected_paths = [[1, 2, 3, 4], [1, 3, 4]]
        self.assertEqual(paths, expected_paths)

    def test_calculate_paths_travel_time(self):
        graph = create_graph(self.stops_df, self.routes_df)
        paths = [[1, 2, 3, 4], [1, 3, 4]]
        paths_travel_time = calculate_paths_travel_time(graph, paths)
        self.assertEqual(len(paths_travel_time), 2)
        self.assertEqual(paths_travel_time[0][0], [1, 2, 3, 4])
        self.assertEqual(paths_travel_time[1][0], [1, 3, 4])

    def test_dijkstra(self):
        graph = create_weighted_graph(self.routes_df)
        path, distance = dijkstra(graph, 1, 4)
        self.assertEqual(path, [1, 3, 4])
        self.assertAlmostEqual(distance, 3.0)

    def test_create_weighted_graph(self):
        weighted_graph = create_weighted_graph(self.routes_df)
        self.assertEqual(len(weighted_graph), 3)
        self.assertIn((2, 1.0), weighted_graph[1])
        self.assertIn((3, 2.0), weighted_graph[1])
        self.assertIn((3, 1.0), weighted_graph[2])
        self.assertIn((4, 1.0), weighted_graph[3])

    def test_calculate_efficiency(self):
        efficiency = calculate_efficiency(10, 5)
        self.assertAlmostEqual(efficiency, 2.0)

if __name__ == '__main__':
    unittest.main()
