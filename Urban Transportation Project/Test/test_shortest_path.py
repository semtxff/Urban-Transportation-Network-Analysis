import unittest
import heapq
import numpy as np
import pandas as pd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import routes_df
from ToolBox.shortest_path import dijkstra, create_graph

class test_shortest_path(unittest.TestCase):
    
    def setUp(self):
        self.graph = create_graph()
        self.start_node = 1
        self.end_node = 2
    
    def test_dijkstra_functionality(self):
        shortest_path, total_distance = dijkstra(self.graph, self.start_node, self.end_node)
        self.assertIsInstance(shortest_path, list)
        self.assertIsInstance(total_distance, np.float64)

    
    def test_heapq_usage(self):
        priority_queue = []
        heapq.heappush(priority_queue, (np.float64(0), self.start_node))
        self.assertIsInstance(priority_queue[0][0], np.float64)
    
    def test_routes_dataframe(self):
        self.assertIsInstance(routes_df, pd.DataFrame)
        self.assertIn('start_stop_id', routes_df.columns)
        self.assertIn('end_stop_id', routes_df.columns)
        self.assertIn('distance', routes_df.columns)
        self.assertEqual(routes_df['distance'].dtype, np.float64)

if __name__ == '__main__':
    unittest.main()