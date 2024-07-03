import tkinter as tk
from tkinter import messagebox
import io
import sys
import os
import pandas as pd
import networkx as nx
import folium
from PyQt5 import QtWidgets, QtWebEngineWidgets, QtCore
import multiprocessing

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

def run_qt_app():
    from ToolBox.GUI import TransportNetworkGUI
    app = QtWidgets.QApplication(sys.argv)
    window = TransportNetworkGUI()
    window.show()
    app.exec_()

def Interactive_Site_Map_function():
    # 使用多进程来运行PyQt应用程序
    process = multiprocessing.Process(target=run_qt_app)
    process.start()

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
    root.title("Traffic network analysis tools")
    root.geometry("400x450")
    tk.Button(root, text="Transportation network graph", command=plt_graph_function).pack(pady=10)
    tk.Button(root, text="GUI", command=Interactive_Site_Map_function).pack(pady=10)
    tk.Button(root, text="Find routes", command=find_routes_function).pack(pady=10)
    tk.Button(root, text="Find highest centrality", command=find_highest_centrality_function).pack(pady=10)
    tk.Button(root, text="Time predict", command=time_predict_function).pack(pady=10)
    tk.Button(root, text="Shortest path", command=shortest_path_function).pack(pady=10)
    tk.Button(root, text="Route effciency", command=route_effciency_function).pack(pady=10)
    tk.Button(root, text="Peak hours traffic analysis", command=Peak_Hours_Traffic_Analysis_function).pack(pady=10)
    tk.Button(root, text="Bus stop utilization analysis", command=Bus_Stop_Utilization_Analysis_function).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_ui()
