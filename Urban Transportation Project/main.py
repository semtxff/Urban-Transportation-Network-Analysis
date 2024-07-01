def directed_graph_function():
    from ToolBox.directed_graph import draw_graph, load_stops_df, load_routes_df, create_graph, node_label, find_most_central_node
    # 使用 draw_graph 函数
    stops_df = load_stops_df()
    routes_df = load_routes_df()
    G = create_graph(stops_df, routes_df)
    labels = node_label()
    draw_graph(G, labels)
    print()
    find_most_central_node(G, labels)

def find_routes_function():
    from ToolBox.find_routes import print_paths, find_all_paths
    from ToolBox.directed_graph import load_routes_df, load_stops_df, node_label, create_graph
    stops_df = load_stops_df()
    routes_df = load_routes_df()
    G = create_graph(stops_df, routes_df)
    print()
    start_node = int(input("Please set start node:"))
    end_node = int(input("Please set end node:"))
    all_paths = find_all_paths(G, start_node, end_node)
    node_labels = node_label()
    print()
    print_paths(all_paths, node_labels)

def route_effciency_function():
    from ToolBox.directed_graph import load_routes_df, load_stops_df
    from ToolBox.route_efficiency import shortest_path, create_and_configure_graph
    stops_df = load_stops_df()
    routes_df = load_routes_df()
    print()
    create_and_configure_graph(stops_df,routes_df)
    shortest_path()

# 运行测试的函数
def run_tests():
    directed_graph_function()
    find_routes_function()
    route_effciency_function()
    print()
    print("All tests passed!")
    print()

# 当该模块被直接运行时，调用run_tests函数
if __name__ == "__main__":
    run_tests()