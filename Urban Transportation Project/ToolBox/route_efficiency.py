import os
import sys
# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.shortest_path import shortest_paths

# 计算总距离
total_distance = shortest_paths[3]  # Bastille 的站点编号为 3

# 假设旅行时间为1小时（可以根据实际情况调整）
travel_time = 1

# 计算效率
efficiency = total_distance / travel_time

print(f"Chatelet 到 Bastille 之间的效率为：{efficiency:.2f}")