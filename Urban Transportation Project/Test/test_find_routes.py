import unittest
from unittest.mock import patch
from io import StringIO
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import routes_df

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

def find_routes(start_node, end_node):
    graph = {}

    for _, row in routes_df.iterrows():
        start_stop_id = row['start_stop_id']
        end_stop_id = row['end_stop_id']

        if start_stop_id not in graph:
            graph[start_stop_id] = []
        graph[start_stop_id].append(end_stop_id)

    visited = {node: False for node in graph}
    path = []

    dfs(graph, start_node, end_node, visited, path)

class test_find_routes(unittest.TestCase):
    
    def setUp(self):
        self.start_node = 1
        self.end_node = 2

    @patch('builtins.input', side_effect=lambda *args: iter([str(self.start_node), str(self.end_node)]))
    @patch('sys.stdout', new_callable=StringIO)
    def test_find_routes_output(self, mock_stdout, mock_input):
        find_routes(self.start_node, self.end_node)
        output = mock_stdout.getvalue().strip()
        expected_output = "Route: [1, np.float64(2.0)]"
        self.assertIn(expected_output, output)
    
    def test_find_routes_functionality(self):
        pass

if __name__ == '__main__':
    unittest.main()
