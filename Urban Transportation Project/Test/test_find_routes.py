import unittest
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from unittest.mock import patch
from io import StringIO

def dfs(graph, start, end, visited, path):
    visited[start] = True
    path.append(start)

    if start == end:
        print("Route:", path)
    else:
        for neighbor in graph.get(start, []):
            if not visited[neighbor]:
                dfs(graph, neighbor, end, visited, path)

    path.pop()
    visited[start] = False

class test_find_routes(unittest.TestCase):
    
    def test_dfs(self):
        mock_input_values = ['1', '5']
        with patch('builtins.input', side_effect=mock_input_values):
            start_node = int(input("输入"))
            end_node = int(input("输入"))
        
        graph = {
            1: [2, 3],
            2: [4],
            3: [5],
            4: [],
            5: []
        }
        visited = {node: False for node in graph}
        path = []

        with patch('sys.stdout', new=StringIO()) as fake_out:
            dfs(graph, start_node, end_node, visited, path)
            printed_output = fake_out.getvalue().strip()
            self.assertIn("Route:", printed_output)

if __name__ == '__main__':
    unittest.main()