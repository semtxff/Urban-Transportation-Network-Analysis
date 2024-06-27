import unittest
import networkx as nx
import pandas as pd

class test_directed_graph(unittest.TestCase):
    def setUp(self):
    
        self.node_labels = {
            1: "Chatelet",
            2: "Gare de Lyon",
            3: "Bastille",
            4: "Nation",
            5: "Opera",
            6: "Republique",
            7: "Montparnasse",
            8: "La Defense",
            9: "Saint-Lazare"
        }

    
        self.stops_df = pd.DataFrame({
            'stop_id': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'longitude': [2.3488, 2.373, 2.369, 2.393, 2.331, 2.363, 2.319, 2.237, 2.324],
            'latitude': [48.853, 48.844, 48.853, 48.847, 48.870, 48.867, 48.839, 48.892, 48.875]
        })

        self.routes_df = pd.DataFrame({
            'start_stop_id': [1, 1, 2, 3, 4, 5, 6, 7, 8],
            'end_stop_id': [2, 5, 3, 4, 6, 6, 7, 8, 9],
            'distance': [1.0, 2.5, 1.5, 1.0, 2.0, 1.2, 1.3, 3.0, 4.0]
        })

    
        self.G = nx.DiGraph()

    
        for _, row in self.stops_df.iterrows():
            self.G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))

        for _, row in self.routes_df.iterrows():
            self.G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])

    def test_nodes(self):
        for _, row in self.stops_df.iterrows():
            self.assertIn(row['stop_id'], self.G.nodes())
            self.assertEqual(self.G.nodes[row['stop_id']]['pos'], (row['longitude'], row['latitude']))

    def test_edges(self):
        for _, row in self.routes_df.iterrows():
            self.assertIn((row['start_stop_id'], row['end_stop_id']), self.G.edges())
            self.assertEqual(self.G.edges[row['start_stop_id'], row['end_stop_id']]['weight'], row['distance'])

    def test_labels(self):
        labels = {node: self.node_labels.get(node, node) for node in self.G.nodes()}
        for node in self.G.nodes():
            self.assertEqual(labels[node], self.node_labels.get(node, node))

if __name__ == '__main__':
    unittest.main()
