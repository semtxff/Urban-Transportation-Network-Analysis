import pandas as pd
import networkx as nx
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets,QtCore
from cv2 import threshold
# 加载数据
stops_df = pd.read_csv('urban_transport_network_stops.csv', names=['start_stop_id', 'end_stop_id', 'distance'])
routes_df = pd.read_csv('urban_transport_network_routes.csv', names=['stop_id', 'name', 'latitude', 'longitude', 'zone_type'])

# 打印列名以确认其正确性
print(stops_df.columns)
print(routes_df.columns)

# 创建交通网络图
G = nx.DiGraph()

# 添加节点
for _, row in routes_df.iterrows():
    G.add_node(row['stop_id'], name=row['name'], pos=(row['latitude'], row['longitude']), zone_type=row['zone_type'])

# 添加边
for _, row in stops_df.iterrows():
    G.add_edge(row['start_stop_id'], row['end_stop_id'], distance=row['distance'])

# 打印列名和数据内容以确认其正确性
print(stops_df.columns)
print(stops_df.head())
print(routes_df.columns)
print(routes_df.head())

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
        self.show_map()
        
        # 添加按钮和功能
        self.initUI()
        
    def initUI(self):
        # 示例：添加按钮
        add_stop_button = QtWidgets.QPushButton('添加站点', self)
        add_stop_button.clicked.connect(self.add_stop)
        add_stop_button.move(10, 10)
        
        # 其他按钮和功能可依此类推
        
    def show_map(self):
        # 将地图保存为HTML文件
        self.map.save('map.html')
        self.webView.setUrl(QtCore.QUrl.fromLocalFile('map.html'))
        
    def add_stop(self):
        # 示例：添加站点的功能
        pass

app = QtWidgets.QApplication([])
window = TransportNetworkGUI()
window.show()
app.exec_()

def optimize_peak_routes(G, peak_data):
    # 示例优化算法
    for start, end in peak_data['routes']:
        path = nx.shortest_path(G, source=start, target=end, weight='distance')
        print(f'Optimized path from {start} to {end}: {path}')

def analyze_stop_utilization(routes_df):
    utilization = routes_df.groupby('stop_id').size()
    low_utilization_stops = utilization[utilization < threshold].index
    return low_utilization_stops