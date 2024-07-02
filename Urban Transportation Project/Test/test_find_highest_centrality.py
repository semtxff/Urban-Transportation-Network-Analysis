import unittest
from unittest.mock import patch
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.find_highest_centrality import find_highest_centrality, print_highest_cretrality

class test_find_highest_centrality(unittest.TestCase):
    
    def setUp(self):
        self.test_graph = {
            1: {'out_degree': 3, 'in_degree': 1, 'name': 'Station A'},
            2: {'out_degree': 2, 'in_degree': 2, 'name': 'Station B'},
            3: {'out_degree': 1, 'in_degree': 1, 'name': 'Station C'}
        }

    def test_find_highest_centrality(self):
        node, degree = find_highest_centrality(self.test_graph)
        self.assertEqual(node, 1)
        self.assertEqual(degree, 4)

    @patch('builtins.print')
    def test_print_highest_cretrality(self, mock_print):
        global G
        G = self.test_graph
        print_highest_cretrality()
        mock_print.assert_called_with('The station with the highest total degree (sum of out-degree and in-degree) is Bastille (3) with 4 connections.')

if __name__ == '__main__':
    unittest.main()
