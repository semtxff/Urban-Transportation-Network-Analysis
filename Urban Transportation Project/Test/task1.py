import os
import sys
# 获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from part1 import ZoneType

# 停车时间估计
parking_times = {
    ZoneType.RESIDENTIAL: 2,
    ZoneType.COMMERCIAL: 4,
    ZoneType.INDUSTRIAL: 3,
    ZoneType.MIXED: 3
}

def calculate_travel_time(stop_a, stop_b):
    # 假设平均速度为每分钟1公里
    average_speed = 1  # 公里/分钟
    distance = G[stop_a.stop_id][stop_b.stop_id]['weight']  # 距离（公里）
    
    # 计算停车时间
    parking_time = parking_times.get(stop_a.zone_type, 0) + parking_times.get(stop_b.zone_type, 0)
    
    # 计算旅行时间
    travel_time = distance / average_speed + parking_time
    return travel_time

# 计算每对站点之间的旅行时间
for stop_pair in itertools.combinations(transport_stops, 2):
    stop_a, stop_b = stop_pair
    travel_time = calculate_travel_time(stop_a, stop_b)
    print(f"Travel time from {stop_a.name} to {stop_b.name}: {travel_time:.2f} minutes")
