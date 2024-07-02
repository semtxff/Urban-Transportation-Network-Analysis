import unittest
import pandas as pd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.route_efficiency import create_graph, calculate_travel_time, find_all_paths, calculate_paths_travel_time, dijkstra, create_weighted_graph, calculate_efficiency

class TestRouteFunctions(unittest.TestCase):
    
    def setUp(self):
        self.stops_df = pd.DataFrame({
            'stop_id': [1, 2, 3],
            'longitude': [10.0, 20.0, 30.0],
            'latitude': [50.0, 60.0, 70.0],
            'name': ['Stop A', 'Stop B', 'Stop C'],
            'zone_type': ['Residential', 'Commercial', 'Industrial']
        })
        
        self.routes_df = pd.DataFrame({
            'start_stop_id': [1, 2],
            'end_stop_id': [2, 3],
            'distance': [10.0, 20.0]
        })
        
    def test_create_graph(self):
        graph = create_graph(self.stops_df, self.routes_df)
        
        self.assertIn(1, graph)
        self.assertEqual(graph[1]['name'], 'Stop A')
        self.assertEqual(graph[1]['zone_type'], 'Residential')
        
    def test_calculate_travel_time(self):
        travel_time = calculate_travel_time(10.0, 'Residential', 'Commercial')
        self.assertAlmostEqual(travel_time, 21.0, delta=0.01)
        
    
if __name__ == '__main__':
    unittest.main()