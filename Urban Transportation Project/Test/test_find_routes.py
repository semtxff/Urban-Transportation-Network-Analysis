import unittest
import networkx as nx
import os
import sys

# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.directed_graph import node_labels
from ToolBox.directed_graph import G

class TestPathFinding(unittest.TestCase):
    def test_find_paths(self):
        start_node = 1  # Chatelet 的节点 ID
        end_node = 3    # Bastille 的节点 ID
        all_paths = list(nx.all_simple_paths(G, source=start_node, target=end_node))
        
        # 验证至少存在一条路径
        self.assertGreater(len(all_paths), 0)
        
        # 可以进一步验证具体路径的内容和顺序，比如：
        expected_paths = [
            ['Chatelet', 'Bastille'],
            # 添加更多预期路径
        ]
        
        found = False
        for path in all_paths:
            path_labels = [node_labels[node] for node in path]
            if set(path_labels) in [set(p) for p in expected_paths]:
                found = True
                break
        
        self.assertTrue(found, f"Expected paths: {expected_paths}. Actual paths found: {[path_labels]}")

if __name__ == '__main__':
    unittest.main()

