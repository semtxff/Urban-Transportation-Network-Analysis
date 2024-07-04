import os
import sys
import pandas as pd
import folium
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets
import heapq
import numpy as np
# Get the directory of the current script file获取当前脚本文件的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import routes_df
routes_df = routes_df[['start_stop_id', 'end_stop_id']]

def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  #The radius of the Earth in kilometers地球半径，单位为千米
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    distance = R * c
    return distance

class TrafficNetworkGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Traffic Network Management System')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create the map创建地图
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        
        # Embed the map into the Qt window将地图嵌入 Qt 窗口
        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.webView)
        
        # Initialize stop data初始化站点数据
        self.stops = {}
        
        # Add initial stops data添加初始站点数据
        self.add_stops_from_csv()
        
        # Show the map显示地图
        self.show_map()
        
        # Add buttons and functionality添加按钮和功能
        self.initUI()
        
        # Undo history撤消历史记录
        self.undo_stack = []
        
        # Initialize route paths list初始化路线路径列表
        self.route_paths = []
        
        # Call function to find and draw routes调用函数查找和绘制路线
        self.find_and_draw_routes()

    def initUI(self):
        # Add example buttons添加示例按钮
        add_stop_button = QtWidgets.QPushButton('Add', self)
        add_stop_button.clicked.connect(self.add_stop)
        add_stop_button.move(50, 10)
        
        remove_stop_button = QtWidgets.QPushButton('Delete', self)
        remove_stop_button.clicked.connect(self.remove_stop)
        remove_stop_button.move(160, 10)
        
        undo_button = QtWidgets.QPushButton('Undelete', self)
        undo_button.clicked.connect(self.undo_remove)
        undo_button.move(270, 10)
        
        show_routes_button = QtWidgets.QPushButton('Show route', self)
        show_routes_button.clicked.connect(self.create_route_buttons)
        show_routes_button.move(380, 10)
        
        # Create a layout for route buttons创建路线按钮的布局
        self.route_buttons_layout = QtWidgets.QVBoxLayout()
        self.route_buttons_widget = QtWidgets.QWidget(self)
        self.route_buttons_widget.setLayout(self.route_buttons_layout)
        self.route_buttons_widget.setGeometry(1000, 50, 150, 700)
        
    
    def add_stops_from_csv(self):
        stops_df = pd.read_csv('urban_transport_network_stops.csv')
        for _, row in stops_df.iterrows():
            stop_id = str(row['stop_id'])
            name = row['name']
            latitude = row['latitude']
            longitude = row['longitude']
            zone_type = row['zone_type']
            
            self.stops[stop_id] = {
                'name': name,
                'latitude': latitude,
                'longitude': longitude,
                'zone_type': zone_type
            }
            
            folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
    
    def show_map(self):
        map_file = 'map.html'
        self.map.save(map_file)
        abs_path = os.path.abspath(map_file)
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(abs_path))
        
    def add_stop(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Add', 'Input Format: stop_id,name,latitude,longitude,zone_type')
        if ok and text:
            stop_info = text.split(',')
            if len(stop_info) == 5:
                stop_id, name, latitude, longitude, zone_type = stop_info
                latitude, longitude = float(latitude), float(longitude)
                
                self.stops[stop_id] = {
                    'name': name,
                    'latitude': latitude,
                    'longitude': longitude,
                    'zone_type': zone_type
                }
                
                folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
                
                self.show_map()
    
    def remove_stop(self):
        text, ok = QtWidgets.QInputDialog.getText(self, 'Delete', 'ID')
        if ok and text:
            stop_id = str(text)
            if stop_id in self.stops:
                self.undo_stack.append((stop_id, self.stops.pop(stop_id)))
                self.update_map_after_removal()
    
    def undo_remove(self):
        if self.undo_stack:
            stop_id, data = self.undo_stack.pop()
            
            self.stops[stop_id] = data
            
            folium.Marker([data['latitude'], data['longitude']], popup=data['name'], tooltip=data['name']).add_to(self.map)
            
            self.show_map()
    
    def update_map_after_removal(self):
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        
        for stop_id, data in self.stops.items():
            folium.Marker([data['latitude'], data['longitude']], popup=data['name'], tooltip=data['name']).add_to(self.map)
        
        self.show_map()
    
    def find_and_draw_routes(self):
        from ToolBox.find_routes import start_node, end_node
        self.start_node = int(start_node)
        self.end_node = int(end_node)
        
        # Create graph from routes_df根据 routes_df 创建图表
        graph = self.create_graph()
        
        # Initialize visited nodes and path list初始化访问节点和路径列表
        visited = {node: False for node in graph}
        path = []
        
        # Clear previous route paths清除以前的路线路径
        self.route_paths = []
        
        # Find routes using DFS使用 DFS 查找路线
        self.dfs_with_path(graph, self.start_node, self.end_node, visited, path)
        
        # Print route paths (for debugging)打印路线路径（用于调试）
    
    def create_graph(self):   
        graph = {}

        for _, row in routes_df.iterrows():
            start_stop_id = row['start_stop_id']
            end_stop_id = row['end_stop_id']

            if start_stop_id not in graph:
                graph[start_stop_id] = []
            graph[start_stop_id].append(end_stop_id)

        return graph
    
    def dfs_with_path(self, graph, start, end, visited, path):
        visited[start] = True
        path.append(start)

        if start == end:
            self.route_paths.append(path.copy())
        else:
            for neighbor in graph.get(start, []):
                if not visited[neighbor]:
                    self.dfs_with_path(graph, neighbor, end, visited, path)

        path.pop()
        visited[start] = False
    
    def create_route_buttons(self):
        # Clear previous buttons清除上一个按钮
        for i in reversed(range(self.route_buttons_layout.count())): 
            widget = self.route_buttons_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Create buttons for each route为每条路线创建按钮
        for idx, _ in enumerate(self.route_paths):
            button = QtWidgets.QPushButton(f'Route {idx + 1}', self)
            button.clicked.connect(lambda _, idx=idx: self.draw_single_route(idx))
            self.route_buttons_layout.addWidget(button)
        
        # Add shortest route button添加最短路线按钮
        shortest_route_button = QtWidgets.QPushButton('Shortest', self)
        shortest_route_button.clicked.connect(self.draw_shortest_route)
        self.route_buttons_layout.addWidget(shortest_route_button)
    
    def draw_single_route(self, route_idx):
        # Clear the map清除地图
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        
        # Draw stops on the map在地图上绘制停靠点
        for stop_id, data in self.stops.items():
            folium.Marker([data['latitude'], data['longitude']], popup=data['name'], tooltip=data['name']).add_to(self.map)
        
        # Draw the selected route on the map在地图上绘制所选路线
        route_path = self.route_paths[route_idx]
        for i in range(len(route_path) - 1):
            start_id = route_path[i]
            end_id = route_path[i + 1]
            start_lat = self.stops.get(str(start_id), {}).get('latitude', None)
            start_lon = self.stops.get(str(start_id), {}).get('longitude', None)
            end_lat = self.stops.get(str(end_id), {}).get('latitude', None)
            end_lon = self.stops.get(str(end_id), {}).get('longitude', None)
            if start_lat is not None and start_lon is not None and end_lat is not None and end_lon is not None:
                folium.PolyLine(locations=[(start_lat, start_lon), (end_lat, end_lon)], color='blue').add_to(self.map)
        
        # Show the updated map显示更新后的地图
        self.show_map()
    
    def draw_shortest_route(self):
        graph = self.create_weighted_graph()
        from ToolBox.find_routes import start_node, end_node
        start_node = int(start_node)
        end_node = int(end_node)
        shortest_path, _ = dijkstra(graph, start_node, end_node)
        
        if shortest_path:
            # Clear the map清除地图
            self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
            
            # Draw stops on the map在地图上绘制停靠点
            for stop_id, data in self.stops.items():
                folium.Marker([data['latitude'], data['longitude']], popup=data['name'], tooltip=data['name']).add_to(self.map)
            
            # Draw the shortest route on the map在地图上绘制最短路线
            for i in range(len(shortest_path) - 1):
                start_id = shortest_path[i]
                end_id = shortest_path[i + 1]
                start_lat = self.stops.get(str(start_id), {}).get('latitude', None)
                start_lon = self.stops.get(str(start_id), {}).get('longitude', None)
                end_lat = self.stops.get(str(end_id), {}).get('latitude', None)
                end_lon = self.stops.get(str(end_id), {}).get('longitude', None)
                if start_lat is not None and start_lon is not None and end_lat is not None and end_lon is not None:
                    folium.PolyLine(locations=[(start_lat, start_lon), (end_lat, end_lon)], color='red').add_to(self.map)
            
            # Show the updated map显示更新后的地图
            self.show_map()
        else:
            QtWidgets.QMessageBox.warning(self, "Warning", "No path was found from the start point to the end point")

    def create_weighted_graph(self):
        graph = {}

        stops_df = pd.read_csv('urban_transport_network_stops.csv')
        stops_dict = {row['stop_id']: (row['latitude'], row['longitude']) for _, row in stops_df.iterrows()}
        
        for _, row in routes_df.iterrows():
            start_stop_id = row['start_stop_id']
            end_stop_id = row['end_stop_id']
            
            if start_stop_id in stops_dict and end_stop_id in stops_dict:
                start_lat, start_lon = stops_dict[start_stop_id]
                end_lat, end_lon = stops_dict[end_stop_id]
                route_length = haversine(start_lat, start_lon, end_lat, end_lon)
                
                if start_stop_id not in graph:
                    graph[start_stop_id] = []
                graph[start_stop_id].append((end_stop_id, route_length))
        
        return graph

def dijkstra(graph, start, end):
    # Creating a priority queue创建一个优先级队列
    priority_queue = []
    heapq.heappush(priority_queue, (0, start))  # (distance, node)
    
    # Create a dictionary to store the shortest distance from the starting point to each node创建一个字典以存储从起点到每个节点的最短距离
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Create a dictionary to store predecessor nodes so that the path can be reconstructed创建一个字典以存储前驱节点，以便重构路径
    previous_nodes = {node: None for node in graph}
    
    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # If the current node is the end point, build and return the path如果当前节点就是终点，构建并返回路径
        if current_node == end:
            path = []
            while previous_nodes[current_node] is not None:
                path.insert(0, current_node)
                current_node = previous_nodes[current_node]
            path.insert(0, start)
            return path, current_distance
        
        # Traverse the neighbors of the current node遍历当前节点的邻居
        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            
            # If a shorter path is found, update the distance and predecessor node, and add the neighbor to the queue如果找到更短的路径，更新距离和前驱节点，并将邻居加入队列
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
    
    return None, float('inf')

# Ensure the main app runs the TrafficNetworkGUI确保主应用程序运行 TrafficNetworkGUI
def run_qt_app():
    app = QtWidgets.QApplication(sys.argv)
    window = TrafficNetworkGUI()
    window.show()
    app.exec_()