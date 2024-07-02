import unittest
import pandas as pd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.time_predict import create_graph, calculate_travel_time, find_all_paths, calculate_paths_travel_time

class test_time_predict(unittest.TestCase):
    
    def setUp(self):
        # 创建示例数据
        self.stops_data = {
            'stop_id': [1, 2, 3],
            'longitude': [120.0, 121.0, 122.0],
            'latitude': [30.0, 31.0, 32.0],
            'name': ['Stop A', 'Stop B', 'Stop C'],
            'zone_type': ['Residential', 'Commercial', 'Industrial']
        }
        self.routes_data = {
            'start_stop_id': [1, 2],
            'end_stop_id': [2, 3],
            'distance': [10.0, 20.0]
        }
        
        self.stops_df = pd.DataFrame(self.stops_data)
        self.routes_df = pd.DataFrame(self.routes_data)
        
        self.graph = create_graph(self.stops_df, self.routes_df)
    
    def test_create_graph(self):
        # 检查创建的图的结构和内容
        self.assertIn(1, self.graph)
        self.assertIn(2, self.graph)
        self.assertIn(3, self.graph)
        
        self.assertEqual(self.graph[1]['name'], 'Stop A')
        self.assertEqual(self.graph[2]['zone_type'], 'Commercial')
        self.assertEqual(self.graph[3]['pos'], (122.0, 32.0))
        
        self.assertIn(2, self.graph[1]['edges'])
        self.assertIn(3, self.graph[2]['edges'])
        
        self.assertEqual(self.graph[1]['edges'][2], 10.0)
        self.assertEqual(self.graph[2]['edges'][3], 20.0)
    
    def test_calculate_travel_time(self):
        # 测试计算旅行时间
        travel_time = calculate_travel_time(10.0, 'Residential', 'Commercial')
        self.assertAlmostEqual(travel_time, 21.0, places=1)  # 10/40*60 + 2 + 4 = 21 minutes
        
        travel_time = calculate_travel_time(20.0, 'Commercial', 'Industrial')
        self.assertAlmostEqual(travel_time, 37.0, places=1)  # 20/40*60 + 4 + 3 = 37 minutes
    
    def test_find_all_paths(self):
        # 测试查找所有路径
        paths = find_all_paths(self.graph, 1, 3)
        self.assertEqual(paths, [[1, 2, 3]])
        
        paths = find_all_paths(self.graph, 1, 2)
        self.assertEqual(paths, [[1, 2]])
        
        paths = find_all_paths(self.graph, 2, 3)
        self.assertEqual(paths, [[2, 3]])
        
        paths = find_all_paths(self.graph, 3, 1)
        self.assertEqual(paths, [])
    
    def test_calculate_paths_travel_time(self):
        # 测试计算路径的总旅行时间
        paths = [[1, 2, 3]]
        paths_travel_time = calculate_paths_travel_time(self.graph, paths)
        self.assertEqual(len(paths_travel_time), 1)
        self.assertAlmostEqual(paths_travel_time[0][1], 58.0, places=1)  # 21.0 + 37.0 = 58.0 minutes

if __name__ == '__main__':
    unittest.main()