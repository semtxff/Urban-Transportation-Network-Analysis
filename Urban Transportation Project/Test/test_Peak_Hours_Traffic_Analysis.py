import unittest
import pandas as pd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.Peak_Hours_Traffic_Analysis import create_graph, analyze_peak_hours_traffic, find_all_paths, calculate_path_time

class test_Peak_Hours_Traffic_Analysis(unittest.TestCase):
    def setUp(self):
        self.stops_df = pd.DataFrame({
            'stop_id': [1, 2, 3],
            'name': ['Stop A', 'Stop B', 'Stop C'],
            'longitude': [0.0, 1.0, 2.0],
            'latitude': [0.0, 1.0, 2.0]
        })
        
        self.routes_df = pd.DataFrame({
            'start_stop_id': [1, 2, 3],
            'end_stop_id': [2, 3, 1],
            'distance': [10.0, 15.0, 20.0]
        })

        self.graph = create_graph(self.stops_df, self.routes_df)
        self.optimized_routes_df = analyze_peak_hours_traffic(self.routes_df, congestion_factor=1.5, stop_delay=2)

    def test_create_graph(self):
        expected_graph = {
            1: {'pos': (0.0, 0.0), 'name': 'Stop A', 'out_degree': 1, 'in_degree': 1, 2: 10.0},
            2: {'pos': (1.0, 1.0), 'name': 'Stop B', 'out_degree': 1, 'in_degree': 1, 3: 15.0},
            3: {'pos': (2.0, 2.0), 'name': 'Stop C', 'out_degree': 1, 'in_degree': 1, 1: 20.0}
        }
        self.assertEqual(self.graph, expected_graph)

    def test_analyze_peak_hours_traffic(self):
        expected_optimized_routes_df = pd.DataFrame({
            'start_stop_id': [1, 2, 3],
            'end_stop_id': [2, 3, 1],
            'distance': [10.0, 15.0, 20.0],
            'peak_hour_distance': [15.0, 22.5, 30.0],
            'peak_hour_time': [3.5, 4.25, 5.0]
        })
        pd.testing.assert_frame_equal(self.optimized_routes_df, expected_optimized_routes_df)

    def test_find_all_paths(self):
        expected_paths = [[1, 2, 3]]
        all_paths = find_all_paths(self.graph, 1, 3)
        self.assertEqual(all_paths, expected_paths)

    def test_calculate_path_time(self):
        path = [1, 2, 3]
        expected_time = 3.5 + 4.25
        total_time = calculate_path_time(self.graph, path, self.optimized_routes_df)
        self.assertEqual(total_time, expected_time)

if __name__ == '__main__':
    unittest.main()