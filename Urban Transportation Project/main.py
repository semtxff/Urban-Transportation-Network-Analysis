def plt_graph_function():
    from ToolBox.plt_graph import plot_transport_network, create_graph, load_routes_df, load_stops_df
    stops_df = load_stops_df("urban_transport_network_stops.csv")
    routes_df = load_routes_df("urban_transport_network_routes.csv")
    my_graph = create_graph(stops_df, routes_df)
    plot_transport_network(my_graph)

def find_routes_function():
    from ToolBox.find_routes import print_paths, find_all_paths
    from ToolBox.directed_graph import load_routes_df, load_stops_df, node_label, create_graph
    stops_df = load_stops_df()
    routes_df = load_routes_df()
    G = create_graph(stops_df, routes_df)
    start_node = int(input("Please set start node:"))
    end_node = int(input("Please set end node:"))
    print()
    all_paths = find_all_paths(G, start_node, end_node)
    node_labels = node_label()
    print_paths(all_paths, node_labels)

def route_effciency_function():
    from ToolBox.directed_graph import load_routes_df, load_stops_df
    from ToolBox.route_efficiency import shortest_path, create_and_configure_graph
    stops_df = load_stops_df()
    routes_df = load_routes_df()
    create_and_configure_graph(stops_df,routes_df)
    shortest_path()

def shortest_path():
    from ToolBox.shortest_path import print_shortest_path
    print_shortest_path()

# 运行测试的函数
def run_tests():
    plt_graph_function()
    print()
    find_routes_function()
    print()
    route_effciency_function()
    print()
    shortest_path()
    print()
    print("All tests passed!")
    print()

# 当该模块被直接运行时，调用run_tests函数
if __name__ == "__main__":
    run_tests()