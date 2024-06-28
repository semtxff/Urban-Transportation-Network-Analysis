import os
import sys
import pandas as pd
import csv
# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.transportstop import ZoneType
from ToolBox.transportstop import TransportStop

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
                zone_type=ZoneType[row['zone_type'].upper()]  # Convert to uppercase and match enum value# 转换为大写并匹配枚举值
            )
            stops.append(stop)
        return stops
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

# File path
csv_file_path = "urban_transport_network_stops.csv"
transport_stops = read_stops_from_csv(csv_file_path)

# Create an empty dictionary to store data创建一个空字典来存储数据
routes_data = {}

# Reading CSV Files读取CSV文件
with open('urban_transport_network_routes.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  
    for row in reader:
        try:
            start_stop_id, end_stop_id, distance = map(int, row)
            routes_data[(start_stop_id, end_stop_id)] = distance
        except ValueError:
            pass  
