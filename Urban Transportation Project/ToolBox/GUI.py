import sys
import os
import pandas as pd
import folium
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets

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
        
        # 初始化站点数据
        self.stops = {}
        
        # 添加初始站点数据
        self.add_stops_from_csv()
        
        # 显示地图
        self.show_map()
        
        # 添加按钮和功能
        self.initUI()
        
        # 撤销历史记录
        self.undo_stack = []

    def initUI(self):
        # 添加按钮示例
        add_stop_button = QtWidgets.QPushButton('添加站点', self)
        add_stop_button.clicked.connect(self.add_stop)
        add_stop_button.move(50, 10)
        
        # 添加删除按钮
        remove_stop_button = QtWidgets.QPushButton('删除站点', self)
        remove_stop_button.clicked.connect(self.remove_stop)
        remove_stop_button.move(160, 10)
        
        # 添加撤销按钮
        undo_button = QtWidgets.QPushButton('撤销删除', self)
        undo_button.clicked.connect(self.undo_remove)
        undo_button.move(270, 10)
        
        # 其他按钮和功能可依此类推
    
    def add_stops_from_csv(self):
        stops_df = pd.read_csv('urban_transport_network_stops.csv')
        # 从CSV文件中读取站点信息并添加到地图和网络图中
        for _, row in stops_df.iterrows():
            stop_id = str(row['stop_id'])
            name = row['name']
            latitude = row['latitude']
            longitude = row['longitude']
            zone_type = row['zone_type']
            
            # 添加到站点字典中
            self.stops[stop_id] = {
                'name': name,
                'latitude': latitude,
                'longitude': longitude,
                'zone_type': zone_type
            }
            
            # 在地图上添加标记
            folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
    
    def show_map(self):
        # 将地图保存为HTML文件并在Qt窗口中显示
        map_file = 'map.html'
        self.map.save(map_file)
        abs_path = os.path.abspath(map_file)
        self.webView.setUrl(QtCore.QUrl.fromLocalFile(abs_path))
        
    def add_stop(self):
        # 弹出对话框获取新站点信息
        text, ok = QtWidgets.QInputDialog.getText(self, '添加站点', '输入格式: stop_id,name,latitude,longitude,zone_type')
        if ok and text:
            stop_info = text.split(',')
            if len(stop_info) == 5:
                stop_id, name, latitude, longitude, zone_type = stop_info
                latitude, longitude = float(latitude), float(longitude)
                
                # 添加到站点字典中
                self.stops[stop_id] = {
                    'name': name,
                    'latitude': latitude,
                    'longitude': longitude,
                    'zone_type': zone_type
                }
                
                # 在地图上添加标记
                folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
                
                # 更新地图显示
                self.show_map()
    
    def remove_stop(self):
        # 弹出对话框获取要删除的站点ID
        text, ok = QtWidgets.QInputDialog.getText(self, '删除站点', '输入要删除的站点ID')
        if ok and text:
            stop_id = str(text)
            if stop_id in self.stops:
                # 将删除操作记录到撤销历史中
                self.undo_stack.append((stop_id, self.stops.pop(stop_id)))
                
                # 更新地图显示
                self.update_map_after_removal()
    
    def undo_remove(self):
        # 恢复最后一次删除操作
        if self.undo_stack:
            stop_id, data = self.undo_stack.pop()
            
            # 添加站点回到站点字典中
            self.stops[stop_id] = data
            
            # 在地图上添加标记
            folium.Marker([data['latitude'], data['longitude']], popup=data['name'], tooltip=data['name']).add_to(self.map)
            
            # 更新地图显示
            self.show_map()
    
    def update_map_after_removal(self):
        # 重新生成地图并显示
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        
        # 添加剩余站点到地图
        for stop_id, data in self.stops.items():
            folium.Marker([data['latitude'], data['longitude']], popup=data['name'], tooltip=data['name']).add_to(self.map)
        
        # 显示更新后的地图
        self.show_map()

def run_qt_app():
    app = QtWidgets.QApplication(sys.argv)
    window = TransportNetworkGUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    run_qt_app()
