import unittest
import sys
import os
# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)
from  ToolBox.read_csv import read_stops_from_csv  # 替换为你实际的脚本文件和函数名
from ToolBox.transportstop import TransportStop, ZoneType

class TestReadStopsFromCSV(unittest.TestCase):
    
    def setUp(self):
        # 设置任何必要的资源或测试数据
        self.csv_file_path = "urban_transport_network_stops.csv"  # 替换为你的测试 CSV 文件路径
    
    def test_read_stops_from_csv_file_not_found(self):
        # 测试文件不存在的情况
        invalid_file_path = "non_existing_file.csv"
        stops = read_stops_from_csv(invalid_file_path)
        self.assertEqual(stops, [], f"期望得到空列表以处理不存在的文件，得到的却是：{stops}")
    
    def test_read_stops_from_csv_valid_file(self):
        # 测试有效的 CSV 文件情况
        stops = read_stops_from_csv(self.csv_file_path)
        self.assertGreater(len(stops), 0, "期望读取到多个停靠点")
        for stop in stops:
            self.assertIsInstance(stop, TransportStop, f"期望得到 TransportStop 实例，得到的却是：{type(stop)}")
    
    def tearDown(self):
        # 在需要时清理资源
        pass

if __name__ == '__main__':
    unittest.main()

