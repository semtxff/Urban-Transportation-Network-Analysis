def test_dev_function1():
    from ToolBox.directed_graph import draw_graph, load_stops_df, load_routes_df, create_graph, node_label, find_most_central_node
    # 使用 draw_graph 函数
    stops_df = load_stops_df()
    routes_df = load_routes_df()
    G = create_graph(stops_df, routes_df)
    labels = node_label()
    draw_graph(G, labels)
    find_most_central_node(G, labels)

def test_dev_function2():
    from ToolBox.find_routes import print_paths, find_all_paths
    from ToolBox.directed_graph import load_routes_df, load_stops_df, node_label, create_graph
    stops_df = load_stops_df()
    routes_df = load_routes_df()
    G = create_graph(stops_df, routes_df)
    start_node = 1
    end_node = 3
    all_paths = find_all_paths(G, start_node, end_node)
    node_labels = node_label()
    print_paths(all_paths, node_labels)
'''
def test_dev_function3():
    result = find_most_central_node
    assert result == "Result of dev_function3", "Test for dev_function3 failed"
'''

# 运行测试的函数
def run_tests():
    test_dev_function1()
    test_dev_function2()
    #test_dev_function3()
    print("All tests passed!")

# 当该模块被直接运行时，调用run_tests函数
if __name__ == "__main__":
    run_tests()