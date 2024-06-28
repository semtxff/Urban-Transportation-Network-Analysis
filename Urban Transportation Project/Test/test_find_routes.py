import unittest
import networkx as nx
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.directed_graph import node_labels
from ToolBox.directed_graph import G

class test_find_routes(unittest.TestCase):
    def test_find_paths(self):
        start_node = 1  
        end_node = 3    
        all_paths = list(nx.all_simple_paths(G, source=start_node, target=end_node))
        
        
        self.assertGreater(len(all_paths), 0)
        
        
        expected_paths = [
            ['Chatelet', 'Bastille'],
            
        ]
        
        found = False
        for path in all_paths:
            path_labels = [node_labels[node] for node in path]
            if set(path_labels) in [set(p) for p in expected_paths]:
                found = True
                break
        
        self.assertTrue(found, f"Expected paths: {expected_paths}. Actual paths found: {[path_labels]}")

if __name__ == '__main__':
    unittest.main()
