import unittest
import csv
import os
import sys
# Gets the directory of the current script file 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# Adds the parent directory (project root) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.transportstop import TransportStop
from ToolBox.transportstop import ZoneType
from ToolBox.transportstop import read_stops_from_csv

class TestTransportStop(unittest.TestCase):
    def test_read_stops_from_csv(self):
        # Create a sample CSV file (you can adjust this based on your actual data)
        csv_content = "stop_id,name,latitude,longitude,zone_type\n1,Stop A,47.123,-122.456,RESIDENTIAL\n2,Stop B,47.456,-122.789,COMMERCIAL"
        with open("sample_stops.csv", "w") as f:
            f.write(csv_content)

        # Test reading stops from the CSV file
        stops = read_stops_from_csv("sample_stops.csv")
        self.assertEqual(len(stops), 2)

        # Check if the first stop is correctly parsed
        self.assertEqual(stops[0].stop_id, 1)
        self.assertEqual(stops[0].name, "Stop A")
        self.assertEqual(stops[0].latitude, 47.123)
        self.assertEqual(stops[0].longitude, -122.456)
        self.assertEqual(stops[0].zone_type, ZoneType.RESIDENTIAL)

        # Clean up the temporary CSV file
        import os
        os.remove("sample_stops.csv")

if __name__ == "__main__":
    unittest.main()
