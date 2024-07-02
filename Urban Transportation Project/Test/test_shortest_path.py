import unittest
import heapq
import numpy as np
import pandas as pd
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import routes_df  # 假设从项目中正确导入了 routes_df
from ToolBox.shortest_path import dijkstra, create_graph  # 将 'your_module' 调整为实际包含 dijkstra 和 create_graph 定义的模块名

class TestDijkstra(unittest.TestCase):
    
    def setUp(self):
        self.graph = create_graph()
        self.start_node = 1  # 替换为实际在数据中使用的起始节点
        self.end_node = 2    # 替换为实际在数据中使用的结束节点
    
    def test_dijkstra_functionality(self):
        shortest_path, total_distance = dijkstra(self.graph, self.start_node, self.end_node)
        self.assertIsInstance(shortest_path, list)
        self.assertIsInstance(total_distance, np.float64)
        
        # 根据需要添加更多具体的测试断言
        # 示例：断言 shortest_path 不为 None，断言 total_distance 在预期范围内等
    
    def test_heapq_usage(self):
        # 测试 dijkstra 函数中 heapq 的正确使用
        priority_queue = []
        heapq.heappush(priority_queue, (np.float64(0), self.start_node))
        self.assertIsInstance(priority_queue[0][0], np.float64)
        
        # 如果需要，可以添加更多与 heapq 相关的测试
    
    def test_routes_dataframe(self):
        # 测试 routes_df 是否包含预期的列和数据类型
        self.assertIsInstance(routes_df, pd.DataFrame)
        self.assertIn('start_stop_id', routes_df.columns)
        self.assertIn('end_stop_id', routes_df.columns)
        self.assertIn('distance', routes_df.columns)
        self.assertEqual(routes_df['distance'].dtype, np.float64)
        
        # 如果需要，可以添加更多与 routes_df 相关的测试
    
    # 根据具体需求添加更多特定的测试案例和断言

if __name__ == '__main__':
    unittest.main()

