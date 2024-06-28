import os
import pandas as pd
import networkx as nx
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore
from opencv import threshold
# Load data 加载数据
stops_df = pd.read_csv('urban_transport_network_stops.csv', names=['start_stop_id', 'end_stop_id', 'distance'])
routes_df = pd.read_csv('urban_transport_network_routes.csv', names=['stop_id', 'name', 'latitude', 'longitude', 'zone_type'])

# Create a traffic network graph 创建交通网络图
G = nx.DiGraph()

# Add node 添加节点
for _, row in routes_df.iterrows():
    G.add_node(row['stop_id'], name=row['name'], pos=(row['latitude'], row['longitude']), zone_type=row['zone_type'])

# Add edge 添加边
for _, row in stops_df.iterrows():
    G.add_edge(row['start_stop_id'], row['end_stop_id'], distance=row['distance'])

class TransportNetworkGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('交通网络管理系统')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create a map 创建地图
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        
        # Embed the map in the Qt window 将地图嵌入到Qt窗口中
        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.webView)
        self.show_map()
        
        # Add buttons and functions 添加按钮和功能
        self.initUI()
        
    def initUI(self):
        add_stop_button = QtWidgets.QPushButton('添加站点', self)
        add_stop_button.clicked.connect(self.add_stop)
        add_stop_button.move(10, 10)
        
    def show_map(self):
        # Save the map as an HTML file 将地图保存为HTML文件
        map_file = 'map.html'
        self.map.save(map_file)
        abs_path = os.path.abspath(map_file)
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(abs_path))
        
    def add_stop(self):
        # A dialog box is displayed to obtain information about the new site 弹出对话框获取新站点信息
        text, ok = QtWidgets.QInputDialog.getText(self, '添加站点', '输入格式: stop_id,name,latitude,longitude,zone_type')
        if ok and text:
            stop_info = text.split(',')
            if len(stop_info) == 5:
                stop_id, name, latitude, longitude, zone_type = stop_info
                latitude, longitude = float(latitude), float(longitude)
                
                # Add to graphic 添加到图形
                G.add_node(stop_id, name=name, pos=(latitude, longitude), zone_type=zone_type)
                
                # Add a new site to the map 在地图上添加新站点
                folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
                self.show_map()

app = QtWidgets.QApplication([])
window = TransportNetworkGUI()
window.show()
app.exec_()

def optimize_peak_routes(G, peak_data):
    for start, end in peak_data['routes']:
        path = nx.shortest_path(G, source=start, target=end, weight='distance')
        print(f'Optimized path from {start} to {end}: {path}')

def analyze_stop_utilization(routes_df):
    utilization = routes_df.groupby('stop_id').size()
    low_utilization_stops = utilization[utilization < threshold].index
    return low_utilization_stops
