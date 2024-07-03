import tkinter as tk
from tkinter import messagebox
import io
import sys
import os
import pandas as pd
import networkx as nx
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore

# 辅助函数，用于捕获打印输出
def capture_print_output(func):
    def wrapper(*args, **kwargs):
        # 创建一个 StringIO 对象来捕获输出
        buffer = io.StringIO()
        # 将 sys.stdout 重定向到 StringIO 对象
        sys.stdout = buffer
        try:
            func(*args, **kwargs)
        finally:
            # 恢复 sys.stdout
            sys.stdout = sys.__stdout__
        # 获取捕获的输出
        return buffer.getvalue()
    return wrapper

def plt_graph_function():
    from ToolBox.plt_graph import plot_transport_network, create_graph, load_routes_df, load_stops_df
    stops_df = load_stops_df("urban_transport_network_stops.csv")
    routes_df = load_routes_df("urban_transport_network_routes.csv")
    my_graph = create_graph(stops_df, routes_df)
    result = capture_print_output(plot_transport_network)(my_graph)

def Interactive_Site_Map_function():
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
            self.G = nx.DiGraph()
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
                
                # 添加到网络图中
                self.G.add_node(stop_id, name=name, pos=(latitude, longitude), zone_type=zone_type)
                
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
                    
                    # 添加到网络图中
                    self.G.add_node(stop_id, name=name, pos=(latitude, longitude), zone_type=zone_type)
                    
                    # 在地图上添加标记
                    folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
                    
                    # 更新地图显示
                    self.show_map()
        
        def remove_stop(self):
            # 弹出对话框获取要删除的站点ID
            text, ok = QtWidgets.QInputDialog.getText(self, '删除站点', '输入要删除的站点ID')
            if ok and text:
                stop_id = str(text)
                if stop_id in self.G.nodes:
                    # 将删除操作记录到撤销历史中
                    self.undo_stack.append((stop_id, self.G.nodes[stop_id]))
                    
                    # 从网络图中移除站点
                    self.G.remove_node(stop_id)
                    
                    # 更新地图显示
                    self.update_map_after_removal(stop_id)
        
        def undo_remove(self):
            # 恢复最后一次删除操作
            if self.undo_stack:
                stop_id, data = self.undo_stack.pop()
                
                # 添加站点回到网络图中
                self.G.add_node(stop_id, **data)
                
                # 在地图上添加标记
                latitude, longitude = data['pos']
                name = data['name']
                folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
                
                # 更新地图显示
                self.show_map()
        
        def update_map_after_removal(self, stop_id):
            # 重新生成地图并显示
            self.map = folium.Map(location=[48.8588443, 2.3470599], zoom_start=13)
            
            # 添加剩余站点到地图
            for node in self.G.nodes(data=True):
                latitude, longitude = node[1]['pos']
                name = node[1]['name']
                folium.Marker([latitude, longitude], popup=name, tooltip=name).add_to(self.map)
            
            # 显示更新后的地图
            self.show_map()

    def run_qt_app():
        app = QtWidgets.QApplication([])
        window = TransportNetworkGUI()
        window.show()
        app.exec_()
    
    result = capture_print_output(run_qt_app)()
    messagebox.showinfo("结果", "互动地图已启动")
    
def find_routes_function():
    from ToolBox.find_routes import create_graph
    result = capture_print_output(create_graph)()
    messagebox.showinfo("结果", result)

def find_highest_centrality_function():
    from ToolBox.find_highest_centrality import print_highest_cretrality
    result = capture_print_output(print_highest_cretrality)()
    messagebox.showinfo("结果", result)

def time_predict_function():
    from ToolBox.time_predict import print_time_predict
    result = capture_print_output(print_time_predict)()
    messagebox.showinfo("结果", result)

def shortest_path_function():
    from ToolBox.shortest_path import print_shortest_path
    result = capture_print_output(print_shortest_path)()
    messagebox.showinfo("结果", result)

def route_effciency_function():
    from ToolBox.route_efficiency import route_efficiency_analysis
    result = capture_print_output(route_efficiency_analysis)()
    messagebox.showinfo("结果", result)

def Peak_Hours_Traffic_Analysis_function():
    from ToolBox.plt_graph import load_routes_df, load_stops_df
    from ToolBox.Peak_Hours_Traffic_Analysis import print_peak_hour_route_between_stops, create_graph, analyze_peak_hours_traffic
    from ToolBox.find_routes import start_node, end_node
    stops_df = load_stops_df("urban_transport_network_stops.csv")
    routes_df = load_routes_df("urban_transport_network_routes.csv")
    G = create_graph(stops_df, routes_df)
    optimized_routes_df = analyze_peak_hours_traffic(routes_df)
    result = capture_print_output(print_peak_hour_route_between_stops)(G, optimized_routes_df, start_node, end_node)
    messagebox.showinfo("结果", result)

def Bus_Stop_Utilization_Analysis_function():
    from ToolBox.Bus_Stop_Utilization_Analysis import print_underutilized_stops, print_recommended_stops
    underutilized_result = capture_print_output(print_underutilized_stops)()
    recommended_result = capture_print_output(print_recommended_stops)()
    result = f"未充分利用的站点: {underutilized_result}\n推荐的新站点: {recommended_result}"
    messagebox.showinfo("结果", result)

def create_ui():
    root = tk.Tk()
    root.title("交通网络分析工具")
    
    tk.Button(root, text="绘制交通网络图", command=plt_graph_function).pack(pady=10)
    tk.Button(root, text="互动地图功能", command=Interactive_Site_Map_function).pack(pady=10)
    tk.Button(root, text="查找路线", command=find_routes_function).pack(pady=10)
    tk.Button(root, text="查找最高中心性", command=find_highest_centrality_function).pack(pady=10)
    tk.Button(root, text="时间预测", command=time_predict_function).pack(pady=10)
    tk.Button(root, text="最短路径计算", command=shortest_path_function).pack(pady=10)
    tk.Button(root, text="路线效率分析", command=route_effciency_function).pack(pady=10)
    tk.Button(root, text="高峰时段交通分析", command=Peak_Hours_Traffic_Analysis_function).pack(pady=10)
    tk.Button(root, text="公交站点利用率分析", command=Bus_Stop_Utilization_Analysis_function).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_ui()
