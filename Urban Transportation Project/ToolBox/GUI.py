import os
import sys
import folium

# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore
from ToolBox.plt_graph import load_routes_df, load_stops_df

def create_graph(stops_df, routes_df):
    graph = {}
    for _, row in stops_df.iterrows():
        stop_id = row['stop_id']
        graph[stop_id] = {
            'pos': (row['latitude'], row['longitude']),
            'name': row['name'],
            'zone_type': row['zone_type'],
            'out_degree': 0,
            'in_degree': 0
        }

    for _, row in routes_df.iterrows():
        start_stop_id = row['start_stop_id']
        end_stop_id = row['end_stop_id']
        distance = row['distance']
        
        if start_stop_id not in graph:
            graph[start_stop_id] = {
                'pos': (0, 0),
                'name': '',
                'zone_type': '',
                'out_degree': 0,
                'in_degree': 0
            }
        if end_stop_id not in graph:
            graph[end_stop_id] = {
                'pos': (0, 0),
                'name': '',
                'zone_type': '',
                'out_degree': 0,
                'in_degree': 0
            }
        
        graph[start_stop_id][end_stop_id] = distance
        graph[start_stop_id]['out_degree'] += 1
        graph[end_stop_id]['in_degree'] += 1
    
    return graph

class TransportNetworkGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('交通网络管理系统')
        self.setGeometry(100, 100, 1200, 800)
        
        # 创建地图
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        
        # 将地图嵌入到Qt窗口中
        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.webView)
        
        # 初始化交通网络图
        self.graph = create_graph(load_stops_df('urban_transport_network_stops.csv'),
                                  load_routes_df('urban_transport_network_routes.csv'))
        self.add_stops_to_map()
        
        # 显示地图
        self.show_map()
        
        # 添加按钮和功能
        self.initUI()
        
        # 撤销历史记录
        self.undo_stack = []
    
    def initUI(self):
        add_stop_button = QtWidgets.QPushButton('添加站点', self)
        add_stop_button.clicked.connect(self.add_stop)
        add_stop_button.move(50, 10)
        
        remove_stop_button = QtWidgets.QPushButton('删除站点', self)
        remove_stop_button.clicked.connect(self.remove_stop)
        remove_stop_button.move(160, 10)
        
        undo_button = QtWidgets.QPushButton('撤销删除', self)
        undo_button.clicked.connect(self.undo_remove)
        undo_button.move(270, 10)
    
    def add_stops_to_map(self):
        for stop_id, data in self.graph.items():
            latitude, longitude = data['pos']
            name = data['name']
            folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
    
    def show_map(self):
        map_file = 'map.html'
        self.map.save(map_file)
        abs_path = os.path.abspath(map_file)
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(abs_path))
        
    def add_stop(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '添加站点', '输入格式: stop_id,name,latitude,longitude,zone_type')
        if ok and text:
            stop_info = text.split(',')
            if len(stop_info) == 5:
                stop_id, name, latitude, longitude, zone_type = stop_info
                latitude, longitude = float(latitude), float(longitude)
                
                self.graph[stop_id] = {
                    'pos': (latitude, longitude),
                    'name': name,
                    'zone_type': zone_type,
                    'out_degree': 0,
                    'in_degree': 0
                }
                
                folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
                self.show_map()
    
    def remove_stop(self):
        text, ok = QtWidgets.QInputDialog.getText(self, '删除站点', '输入要删除的站点ID')
        if ok and text:
            stop_id = str(text)
            if stop_id in self.graph:
                self.undo_stack.append((stop_id, self.graph.pop(stop_id)))
                self.update_map_after_removal(stop_id)
    
    def undo_remove(self):
        if self.undo_stack:
            stop_id, data = self.undo_stack.pop()
            self.graph[stop_id] = data
            latitude, longitude = data['pos']
            name = data['name']
            folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
            self.show_map()
    
    def update_map_after_removal(self, stop_id):
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        for stop_id, data in self.graph.items():
            latitude, longitude = data['pos']
            name = data['name']
            folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
        self.show_map()
