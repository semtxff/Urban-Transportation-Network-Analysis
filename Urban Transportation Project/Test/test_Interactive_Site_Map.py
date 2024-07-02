import unittest
import pandas as pd
from unittest.mock import patch
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

class test_Interactive_Site_Map(unittest.TestCase):

    @patch("builtins.print")
    @patch("pandas.read_csv")
    @patch("folium.Map.save")
    def test_add_map(self, mock_save, mock_read_csv, mock_print):
        mock_data = pd.DataFrame({
            'latitude': [40.7128, 34.0522, 41.8781],
            'longitude': [-74.0060, -118.2437, -87.6298],
            'name': ['Stop 1', 'Stop 2', 'Stop 3'],
            'zone_type': ['Zone A', 'Zone B', 'Zone C']
        })
        mock_read_csv.return_value = mock_data

        # 调用原函数
        from ToolBox.Interactive_Site_Map import add_map
        add_map()

        mock_read_csv.assert_called_once_with("urban_transport_network_stops.csv")

        mock_save.assert_called_once_with("interactive_transport_network_map.html")

        mock_print.assert_called_once_with("interactive_transport.network_map.html has been successfully added!")

if __name__ == "__main__":
    unittest.main()