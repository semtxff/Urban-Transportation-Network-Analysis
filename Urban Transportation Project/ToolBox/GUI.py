import os
import sys
import pandas as pd
import folium
from PyQt5 import QtWidgets, QtCore, QtWebEngineWidgets

# Get the directory of the current script file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.plt_graph import routes_df
routes_df = routes_df[['start_stop_id', 'end_stop_id']]

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
        
        # Initialize route paths list
        self.route_paths = []
        
        # Call function to find and draw routes
        self.find_and_draw_routes()

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
        
        show_routes_button = QtWidgets.QPushButton('显示路线', self)
        show_routes_button.clicked.connect(self.create_route_buttons)
        show_routes_button.move(380, 10)
        
        # Create a layout for route buttons
        self.route_buttons_layout = QtWidgets.QVBoxLayout()
        self.route_buttons_widget = QtWidgets.QWidget(self)
        self.route_buttons_widget.setLayout(self.route_buttons_layout)
        self.route_buttons_widget.setGeometry(1000, 50, 150, 700)
        
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
    
    def find_and_draw_routes(self):
        from ToolBox.find_routes import start_node, end_node
        self.start_node = int(start_node)
        self.end_node = int(end_node)
        
        # Create graph from routes_df
        graph = self.create_graph()
        
        # Initialize visited nodes and path list
        visited = {node: False for node in graph}
        path = []
        
        # Clear previous route paths
        self.route_paths = []
        
        # Find routes using DFS
        self.dfs_with_path(graph, self.start_node, self.end_node, visited, path)
        
        # Print route paths (for debugging)
    
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
        # Clear previous buttons
        for i in reversed(range(self.route_buttons_layout.count())): 
            widget = self.route_buttons_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        
        # Create buttons for each route
        for idx, _ in enumerate(self.route_paths):
            button = QtWidgets.QPushButton(f'路线 {idx + 1}', self)
            button.clicked.connect(lambda _, idx=idx: self.draw_single_route(idx))
            self.route_buttons_layout.addWidget(button)
    
    def draw_single_route(self, route_idx):
        # Clear the map
        self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
        
        # Draw stops on the map
        for stop_id, data in self.stops.items():
            folium.Marker([data['latitude'], data['longitude']], popup=data['name'], tooltip=data['name']).add_to(self.map)
        
        # Draw the selected route on the map
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
        
        # Show the updated map
        self.show_map()

# Ensure the main app runs the TrafficNetworkGUI
def run_qt_app():
    app = QtWidgets.QApplication(sys.argv)
    window = TrafficNetworkGUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    run_qt_app()
