def plt_graph_function():
    from ToolBox.plt_graph import plot_transport_network, create_graph, load_routes_df, load_stops_df
    stops_df = load_stops_df("urban_transport_network_stops.csv")
    routes_df = load_routes_df("urban_transport_network_routes.csv")
    my_graph = create_graph(stops_df, routes_df)
    plot_transport_network(my_graph)


def find_highest_centrality_function():
    from ToolBox.find_highest_centrality import print_highest_cretrality
    print_highest_cretrality()


def find_routes_function():
    from ToolBox.find_routes import create_graph
    create_graph()


def time_predict_function():
    from ToolBox.time_predict import print_time_predict
    print_time_predict()


def shortest_path_function():
    from ToolBox.shortest_path import print_shortest_path
    print_shortest_path()


def route_effciency_function():
    from ToolBox.route_efficiency import route_efficiency_analysis
    route_efficiency_analysis()


def Interactive_Site_Map_function():
    from ToolBox.Interactive_Site_Map import add_map
    add_map()


def Peak_Hours_Traffic_Analysis_function():
    from ToolBox.plt_graph import stops_df, routes_df
    from ToolBox.Peak_Hours_Traffic_Analysis import print_peak_hour_route_between_stops, create_graph, analyze_peak_hours_traffic
    from ToolBox.find_routes import start_node, end_node
    G = create_graph(stops_df, routes_df)
    optimized_routes_df = analyze_peak_hours_traffic(routes_df)
    print_peak_hour_route_between_stops(G, optimized_routes_df, start_node, end_node)


def Bus_Stop_Utilization_Analysis_function():
    from ToolBox.Bus_Stop_Utilization_Analysis import print_underutilized_stops, print_recommended_stops
    print_underutilized_stops()
    print_recommended_stops()



# 运行测试的函数
def run_tests():
    plt_graph_function()
    print()
    print("\033[94mfind highest centrality function:\033[0m")
    find_highest_centrality_function()
    print()
    print("\033[94mfind routes function:\033[0m")
    find_routes_function()
    print()
    print("\033[94mtime predict function:\033[0m")
    time_predict_function()
    print()
    print("\033[94mshortest path function:\033[0m")
    shortest_path_function()
    print()
    print("\033[94mroute effciency function:\033[0m")
    route_effciency_function()
    print()
    print("\033[94mInteractive Site Map function:\033[0m")
    Interactive_Site_Map_function()
    print()
    print("\033[94mPeak Hours Traffic Analysis function:\033[0m")
    Peak_Hours_Traffic_Analysis_function()
    print()
    print("\033[94mBus Stop Utilization Analysis function:\033[0m")
    Bus_Stop_Utilization_Analysis_function()
    print()
    print("\033[92mAll tests passed!\033[0m")
    print()

# 当该模块被直接运行时，调用run_tests函数
if __name__ == "__main__":
    run_tests()