import unittest
import pandas as pd
import os
import sys

# Get the directory of the current script file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.route_efficiency import create_graph, calculate_travel_time, find_all_paths, dijkstra, create_weighted_graph, calculate_paths_travel_time, calculate_efficiency

class TestTransportNetworkFunctions(unittest.TestCase):
    
    def setUp(self):
        # Setup test data
        stops_data = {
            'stop_id': [1, 2, 3],
            'longitude': [0, 1, 2],
            'latitude': [0, 1, 2],
            'name': ['Stop A', 'Stop B', 'Stop C'],
            'zone_type': ['Residential', 'Commercial', 'Industrial']
        }
        routes_data = {
            'start_stop_id': [1, 2],
            'end_stop_id': [2, 3],
            'distance': [10, 20]
        }
        self.stops_df = pd.DataFrame(stops_data)
        self.routes_df = pd.DataFrame(routes_data)
    
    def test_create_graph(self):
        graph = create_graph(self.stops_df, self.routes_df)
        self.assertEqual(len(graph), 3)  # Assuming three stops in the test data
    
    def test_find_all_paths(self):
        graph = create_graph(self.stops_df, self.routes_df)
        paths = find_all_paths(graph, 1, 3)
        self.assertEqual(len(paths), 1)  # Assuming only one path exists in the test data
    
    def test_calculate_paths_travel_time(self):
        graph = create_graph(self.stops_df, self.routes_df)
        paths = find_all_paths(graph, 1, 3)
        paths_travel_times = calculate_paths_travel_time(graph, paths)
        self.assertEqual(len(paths_travel_times), 1)  # Assuming one valid path exists
    
    def test_calculate_efficiency(self):
        total_distance = 30  # Example total distance
        travel_time = 20  # Example travel time
        efficiency = calculate_efficiency(total_distance, travel_time)
        self.assertAlmostEqual(efficiency, 1.5, places=1)  # Adjust based on your calculation

if __name__ == '__main__':
    unittest.main()
