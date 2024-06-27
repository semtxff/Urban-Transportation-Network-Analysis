import unittest
import csv
import os
import sys
# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.transportstop import TransportStop
from ToolBox.transportstop import ZoneType
from ToolBox.transportstop import read_transport_stops_from_csv

class TestTransportStop(unittest.TestCase):
    def test_stop_creation(self):
        # Create a sample TransportStop
        stop = TransportStop(stop_id=1, name="Sample Stop", latitude=40.7128, longitude=-74.0060, zone_type=ZoneType.RESIDENTIAL)
        self.assertEqual(stop.stop_id, 1)
        self.assertEqual(stop.name, "Sample Stop")
        self.assertEqual(stop.latitude, 40.7128)
        self.assertEqual(stop.longitude, -74.0060)
        self.assertEqual(stop.zone_type, ZoneType.RESIDENTIAL)

    def test_invalid_zone_type(self):
        # Ensure ValueError is raised for invalid zone_type
        with self.assertRaises(ValueError):
            TransportStop(stop_id=2, name="Invalid Stop", latitude=35.6895, longitude=139.6917, zone_type="INVALID")

def read_transport_stops_from_csv(filename):
    stops = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                start_stop_id = int(row['start_stop_id'])
                end_stop_id = int(row['end_stop_id'])  # 注意这里要转换为整数
                distance = float(row['distance'])

                # 创建 TransportStop 对象并添加到列表中
                stop = TransportStop(stop_id=start_stop_id, name=row['name'], latitude=row['latitude'], longitude=row['longitude'], zone_type=row['zone_type'])
                stops.append(stop)
            except ValueError:
                print(f"Error processing row: {row}")
    return stops


if __name__ == "__main__":
    unittest.main()
