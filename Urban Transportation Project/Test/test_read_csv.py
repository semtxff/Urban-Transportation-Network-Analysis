import unittest
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from  ToolBox.read_csv import read_stops_from_csv  
from ToolBox.transportstop import TransportStop, ZoneType

class test_read_csv(unittest.TestCase):
    
    def setUp(self):
        self.csv_file_path = "urban_transport_network_stops.csv" 
    
    def test_read_stops_from_csv_file_not_found(self):
        invalid_file_path = "non_existing_file.csv"
        stops = read_stops_from_csv(invalid_file_path)
        self.assertEqual(stops, [], f"期望得到空列表以处理不存在的文件，得到的却是：{stops}")
    
    def test_read_stops_from_csv_valid_file(self):
        stops = read_stops_from_csv(self.csv_file_path)
        self.assertGreater(len(stops), 0, "期望读取到多个停靠点")
        for stop in stops:
            self.assertIsInstance(stop, TransportStop, f"期望得到 TransportStop 实例，得到的却是：{type(stop)}")
    
    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()