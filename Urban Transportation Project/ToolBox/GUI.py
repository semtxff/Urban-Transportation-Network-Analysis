import sys
import os
import pandas as pd
import folium
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets

# Rename the class to avoid conflicts
class TrafficNetworkGUI(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('交通网络管理系统')
        self.setGeometry(100, 100, 1200, 800)
        
        # Create the map
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        
        # Embed the map into the Qt window
        self.webView = QtWebEngineWidgets.QWebEngineView()
        self.setCentralWidget(self.webView)
        
        # Initialize stop data
        self.stops = {}
        
        # Add initial stops data
        self.add_stops_from_csv()
        
        # Show the map
        self.show_map()
        
        # Add buttons and functionality
        self.initUI()
        
        # Undo history
        self.undo_stack = []

    def initUI(self):
        # Add example buttons
        add_stop_button = QtWidgets.QPushButton('添加站点', self)
        add_stop_button.clicked.connect(self.add_stop)
        add_stop_button.move(50, 10)
        
        remove_stop_button = QtWidgets.QPushButton('删除站点', self)
        remove_stop_button.clicked.connect(self.remove_stop)
        remove_stop_button.move(160, 10)
        
        undo_button = QtWidgets.QPushButton('撤销删除', self)
        undo_button.clicked.connect(self.undo_remove)
        undo_button.move(270, 10)
        
        # Other buttons and functionalities can be added here
    
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
        text, ok = QtWidgets.QInputDialog.getText(self, '添加站点', '输入格式: stop_id,name,latitude,longitude,zone_type')
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
        text, ok = QtWidgets.QInputDialog.getText(self, '删除站点', '输入要删除的站点ID')
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

# Ensure the main app runs the TrafficNetworkGUI
def run_qt_app():
    app = QtWidgets.QApplication(sys.argv)
    window = TrafficNetworkGUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    run_qt_app()

