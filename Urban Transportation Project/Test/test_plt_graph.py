import unittest
import pandas as pd
from io import StringIO
import matplotlib.pyplot as plt
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import load_stops_df, load_routes_df, create_graph, plot_transport_network

class test_plt_graph(unittest.TestCase):

    def setUp(self):
        self.stops_data_str = """stop_id,longitude,latitude,name
        1,10.0,20.0,Stop1
        2,20.0,30.0,Stop2
        3,30.0,40.0,Stop3"""
        
        self.routes_data_str = """start_stop_id,end_stop_id,distance
        1,2,10.0
        2,3,20.0
        3,1,30.0"""

    def test_load_stops_df(self):
        stops_data = StringIO(self.stops_data_str)
        stops_df = load_stops_df(stops_data)
        expected_stops_df = pd.read_csv(StringIO(self.stops_data_str))
        pd.testing.assert_frame_equal(stops_df, expected_stops_df)

    def test_load_routes_df(self):
        routes_data = StringIO(self.routes_data_str)
        routes_df = load_routes_df(routes_data)
        expected_routes_df = pd.read_csv(StringIO(self.routes_data_str))
        pd.testing.assert_frame_equal(routes_df, expected_routes_df)

    def test_create_graph(self):
        stops_df = pd.read_csv(StringIO(self.stops_data_str))
        routes_df = pd.read_csv(StringIO(self.routes_data_str))
        graph = create_graph(stops_df, routes_df)
        expected_graph = {
            1: {'pos': (10.0, 20.0), 'name': 'Stop1', 'out_degree': 1, 'in_degree': 1, 2: 10.0},
            2: {'pos': (20.0, 30.0), 'name': 'Stop2', 'out_degree': 1, 'in_degree': 1, 3: 20.0},
            3: {'pos': (30.0, 40.0), 'name': 'Stop3', 'out_degree': 1, 'in_degree': 1, 1: 30.0}
        }
        self.assertEqual(graph, expected_graph)

    def test_plot_transport_network(self):
        stops_df = pd.read_csv(StringIO(self.stops_data_str))
        routes_df = pd.read_csv(StringIO(self.routes_data_str))
        graph = create_graph(stops_df, routes_df)
        plt.figure()
        plot_transport_network(graph)

if __name__ == '__main__':
    unittest.main()
