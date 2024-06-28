import unittest
import networkx as nx
import pandas as pd
from io import StringIO

class test_directed_graph(unittest.TestCase):
    def setUp(self):
        
        self.stops_data = StringIO("""stop_id,longitude,latitude
1,2.3522,48.8566
2,2.3731,48.8442
3,2.3690,48.8530
4,2.3925,48.8470
5,2.3318,48.8686
6,2.3625,48.8670
7,2.3204,48.8422
8,2.2374,48.8914
9,2.3247,48.8765""")
        
        self.routes_data = StringIO("""start_stop_id,end_stop_id,distance
1,2,3.5
1,3,2.1
2,4,4.0
3,4,1.2
4,5,2.8
5,6,3.3
6,7,4.1
7,8,5.7
8,9,6.2
9,1,7.3""")
        
        self.node_labels = {1:"Chatelet", 2:"Gare de Lyon", 3:"Bastille", 4:"Nation", 5:"Opera", 6:"Republique", 7:"Montparnasse", 8:"La Defense", 9:"Saint-Lazare"}

    def test_network_graph(self):
        
        stops_df = pd.read_csv(self.stops_data)
        routes_df = pd.read_csv(self.routes_data)

        
        G = nx.DiGraph()

        
        for _, row in stops_df.iterrows():
            G.add_node(row['stop_id'], pos=(row['longitude'], row['latitude']))

        for _, row in routes_df.iterrows():
            G.add_edge(row['start_stop_id'], row['end_stop_id'], weight=row['distance'])

        labels = {node: self.node_labels.get(node, node) for node in G.nodes()}

        
        degree_centrality = nx.degree_centrality(G)

        
        max_centrality = max(degree_centrality.values())
        most_central_node = [node for node, centrality in degree_centrality.items() if centrality == max_centrality]
        
        self.assertEqual(labels[most_central_node[0]], "Chatelet")
        self.assertEqual(most_central_node[0], 1)

if __name__ == '__main__':
    unittest.main()