import csv
import os
import sys
import pandas as pd
# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.read_csv import read_stops_from_csv

class Stop:
    def __init__(self, stop_id, name, latitude, longitude, zone_type):
        self.stop_id = stop_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.zone_type = zone_type

    def __repr__(self):
        return f"Stop({self.stop_id}, '{self.name}', {self.latitude}, {self.longitude}, '{self.zone_type}')"

    def __eq__(self, other):
        return isinstance(other, Stop) and vars(self) == vars(other)

    def __lt__(self, other):
        return isinstance(other, Stop) and self.stop_id < other.stop_id

csv_file_path = "urban_transport_network_stops.csv"
transport_stops = read_stops_from_csv(csv_file_path)

for stop in transport_stops:
    print(stop)
