import tkinter as tk
from tkinter import messagebox

def plt_graph_function():
    from ToolBox.plt_graph import plot_transport_network, create_graph, load_routes_df, load_stops_df
    stops_df = load_stops_df("urban_transport_network_stops.csv")
    routes_df = load_routes_df("urban_transport_network_routes.csv")
    my_graph = create_graph(stops_df, routes_df)
    plot_transport_network(my_graph)
    messagebox.showinfo("结果", "绘制交通网络图完成！")

def find_highest_centrality_function():
    from ToolBox.find_highest_centrality import print_highest_cretrality
    print_highest_cretrality()
    messagebox.showinfo("结果", "查找最高中心性完成！")

def find_routes_function():
    from ToolBox.find_routes import create_graph
    create_graph()
    messagebox.showinfo("结果", "查找路线完成！")

def time_predict_function():
    from ToolBox.time_predict import print_time_predict
    print_time_predict()
    messagebox.showinfo("结果", "时间预测完成！")

def shortest_path_function():
    from ToolBox.shortest_path import print_shortest_path
    print_shortest_path()
    messagebox.showinfo("结果", "最短路径计算完成！")

def route_effciency_function():
    from ToolBox.route_efficiency import route_efficiency_analysis
    route_efficiency_analysis()
    messagebox.showinfo("结果", "路线效率分析完成！")

def Interactive_Site_Map_function():
    from ToolBox.Interactive_Site_Map import add_map
    add_map()
    messagebox.showinfo("结果", "互动地图功能完成！")

def Peak_Hours_Traffic_Analysis_function():
    from ToolBox.plt_graph import stops_df, routes_df
    from ToolBox.Peak_Hours_Traffic_Analysis import print_peak_hour_route_between_stops, create_graph, analyze_peak_hours_traffic
    from ToolBox.find_routes import start_node, end_node
    G = create_graph(stops_df, routes_df)
    optimized_routes_df = analyze_peak_hours_traffic(routes_df)
    print_peak_hour_route_between_stops(G, optimized_routes_df, start_node, end_node)
    messagebox.showinfo("结果", "高峰时段交通分析完成！")

def Bus_Stop_Utilization_Analysis_function():
    from ToolBox.Bus_Stop_Utilization_Analysis import print_underutilized_stops, print_recommended_stops
    print_underutilized_stops()
    print_recommended_stops()
    messagebox.showinfo("结果", "公交站点利用率分析完成！")

def create_ui():
    root = tk.Tk()
    root.title("交通网络分析工具")
    
    tk.Button(root, text="绘制交通网络图", command=plt_graph_function).pack(pady=10)
    tk.Button(root, text="查找最高中心性", command=find_highest_centrality_function).pack(pady=10)
    tk.Button(root, text="查找路线", command=find_routes_function).pack(pady=10)
    tk.Button(root, text="时间预测", command=time_predict_function).pack(pady=10)
    tk.Button(root, text="最短路径计算", command=shortest_path_function).pack(pady=10)
    tk.Button(root, text="路线效率分析", command=route_effciency_function).pack(pady=10)
    tk.Button(root, text="互动地图功能", command=Interactive_Site_Map_function).pack(pady=10)
    tk.Button(root, text="高峰时段交通分析", command=Peak_Hours_Traffic_Analysis_function).pack(pady=10)
    tk.Button(root, text="公交站点利用率分析", command=Bus_Stop_Utilization_Analysis_function).pack(pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_ui()
