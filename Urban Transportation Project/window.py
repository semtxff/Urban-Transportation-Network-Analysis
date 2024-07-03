import sys
import multiprocessing
from io import StringIO
from contextlib import redirect_stdout
from PyQt5 import QtWidgets, QtCore

# 导入功能模块
from ToolBox.plt_graph import plot_transport_network, create_graph as create_graph_plot, load_routes_df, load_stops_df
from ToolBox.find_routes import create_graph as create_graph_routes
from ToolBox.find_highest_centrality import print_highest_cretrality
from ToolBox.time_predict import print_time_predict
from ToolBox.shortest_path import print_shortest_path
from ToolBox.route_efficiency import route_efficiency_analysis
from ToolBox.Interactive_Site_Map import add_map
from ToolBox.Peak_Hours_Traffic_Analysis import print_peak_hour_route_between_stops, analyze_peak_hours_traffic
from ToolBox.find_routes import start_node, end_node
from ToolBox.Bus_Stop_Utilization_Analysis import print_underutilized_stops, print_recommended_stops

class TransportNetworkGUI(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()

        self.buttons = {
            "Plot Graph": self.plt_graph_function,
            "Find Routes": self.find_routes_function,
            "Find Highest Centrality": self.find_highest_centrality_function,
            "Time Predict": self.time_predict_function,
            "Shortest Path": self.shortest_path_function,
            "Route Efficiency": self.route_effciency_function,
            "Interactive Site Map": self.Interactive_Site_Map_function,
            "Peak Hours Traffic Analysis": self.Peak_Hours_Traffic_Analysis_function,
            "Bus Stop Utilization Analysis": self.Bus_Stop_Utilization_Analysis_function,
            "Reset Node": self.reset_node_function  # 添加Reset Node按钮
        }

        for name, func in self.buttons.items():
            button = QtWidgets.QPushButton(name, self)
            button.clicked.connect(func)
            layout.addWidget(button)

        self.setLayout(layout)
        self.setWindowTitle('Transport Network GUI')
        self.setGeometry(300, 300, 300, 200)

    def show_output(self, output):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setWindowTitle("Output")
        msg_box.setText(output)
        msg_box.exec_()

    def capture_output(self, func):
        f = StringIO()
        with redirect_stdout(f):
            func()
        return f.getvalue()

    def plt_graph_function(self):
        stops_df = load_stops_df("urban_transport_network_stops.csv")
        routes_df = load_routes_df("urban_transport_network_routes.csv")
        my_graph = create_graph_plot(stops_df, routes_df)
        plot_transport_network(my_graph)

    def find_routes_function(self):
        output = self.capture_output(create_graph_routes)
        self.show_output(output)

    def find_highest_centrality_function(self):
        output = self.capture_output(print_highest_cretrality)
        self.show_output(output)

    def time_predict_function(self):
        output = self.capture_output(print_time_predict)
        self.show_output(output)

    def shortest_path_function(self):
        output = self.capture_output(print_shortest_path)
        self.show_output(output)

    def route_effciency_function(self):
        output = self.capture_output(route_efficiency_analysis)
        self.show_output(output)

    def Interactive_Site_Map_function(self):
        output = self.capture_output(add_map)
        self.show_output(output)

    def Peak_Hours_Traffic_Analysis_function(self):
        output = self.capture_output(self._Peak_Hours_Traffic_Analysis_function)
        self.show_output(output)

    def _Peak_Hours_Traffic_Analysis_function(self):
        stops_df = load_stops_df("urban_transport_network_stops.csv")
        routes_df = load_routes_df("urban_transport_network_routes.csv")
        G = create_graph_plot(stops_df, routes_df)
        optimized_routes_df = analyze_peak_hours_traffic(routes_df)
        print_peak_hour_route_between_stops(G, optimized_routes_df, start_node, end_node)

    def Bus_Stop_Utilization_Analysis_function(self):
        output = self.capture_output(self._Bus_Stop_Utilization_Analysis_function)
        self.show_output(output)

    def _Bus_Stop_Utilization_Analysis_function(self):
        print_underutilized_stops()
        print_recommended_stops()

    def reset_node_function(self):
        QtCore.QCoreApplication.quit()
        QtCore.QProcess.startDetached(sys.executable, sys.argv)

def run_qt_app():
    app = QtWidgets.QApplication(sys.argv)
    window = TransportNetworkGUI()
    window.show()
    app.exec_()

if __name__ == "__main__":
    run_qt_app()
