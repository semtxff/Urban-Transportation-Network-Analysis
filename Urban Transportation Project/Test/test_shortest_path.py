import unittest
import networkx as nx
import pandas as pd

class test_shortest_path(unittest.TestCase):
        
    def setUp(self):
        self.stops_df = pd.read_csv("urban_transport_network_stops.csv")
        self.routes_df = pd.read_csv("urban_transport_network_routes.csv")
        self.G = nx.DiGraph()
        
        for _, row in self.stops_df.iterrows():
            self.G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))
        
        for _, row in self.routes_df.iterrows():
            self.G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])
    
    def test_shortest_path_distance(self):
        shortest_paths = nx.single_source_dijkstra_path_length(self.G, source=1, weight='weight')
        self.assertEqual(shortest_paths[2], 10.5)
    
    def test_shortest_path_nodes(self):
        shortest_paths = nx.single_source_dijkstra_path(self.G, source=1, weight='weight')
        self.assertEqual(shortest_paths[2], [1, 2])

if __name__ == '__main__':
    unittest.main()