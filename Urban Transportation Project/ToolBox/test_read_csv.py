import os
import sys
import pandas as pd
import csv
import unittest
from unittest.mock import patch, mock_open
from io import StringIO
from enum import Enum

# Simulate the ZoneType enumeration 模拟 ZoneType 枚举 
class ZoneType(Enum):
    ZONE1 = 1
    ZONE2 = 2

class TransportStop:
    def __init__(self, stop_id, name, latitude, longitude, zone_type):
        self.stop_id = stop_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.zone_type = zone_type

# Gets the directory of the current script file 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# Adds the parent directory (project root) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

def read_stops_from_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        stops = []
        for _, row in data.iterrows():
            stop = TransportStop(
                stop_id=row['stop_id'],
                name=row['name'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                zone_type=ZoneType[row['zone_type'].upper()]  # Convert to uppercase and match enum value
            )
            stops.append(stop)
        return stops
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

def read_routes_from_csv(file_path):
    routes_data = {}
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            try:
                start_stop_id, end_stop_id, distance = map(int, row)
                routes_data[(start_stop_id, end_stop_id)] = distance
            except ValueError:
                pass
    return routes_data

# Unittest code 单元测试代码
class TestTransportData(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open, read_data="stop_id,name,latitude,longitude,zone_type\n1,StopA,12.34,56.78,zone1\n2,StopB,23.45,67.89,zone2")
    def test_read_stops_from_csv(self, mock_file):
        with patch('pandas.read_csv', return_value=pd.read_csv(StringIO(mock_file().read()))):
            stops = read_stops_from_csv("fake_path.csv")
            self.assertEqual(len(stops), 2)
            self.assertEqual(stops[0].stop_id, 1)
            self.assertEqual(stops[0].name, "StopA")
            self.assertEqual(stops[0].latitude, 12.34)
            self.assertEqual(stops[0].longitude, 56.78)
            self.assertEqual(stops[0].zone_type, ZoneType.ZONE1)
            self.assertEqual(stops[1].stop_id, 2)
            self.assertEqual(stops[1].name, "StopB")
            self.assertEqual(stops[1].latitude, 23.45)
            self.assertEqual(stops[1].longitude, 67.89)
            self.assertEqual(stops[1].zone_type, ZoneType.ZONE2)

    @patch("builtins.open", new_callable=mock_open, read_data="start_stop_id,end_stop_id,distance\n1,2,100\n2,3,200")
    def test_read_routes_from_csv(self, mock_file):
        routes = read_routes_from_csv("fake_path.csv")
        self.assertEqual(len(routes), 2)
        self.assertEqual(routes[(1, 2)], 100)
        self.assertEqual(routes[(2, 3)], 200)

if __name__ == "__main__":
    unittest.main()
