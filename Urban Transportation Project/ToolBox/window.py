import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ToolBox.plt_graph import plot_transport_network, create_graph, load_routes_df, load_stops_df
from ToolBox.find_highest_centrality import print_highest_cretrality
from ToolBox.find_routes import create_graph as create_routes_graph
from ToolBox.time_predict import print_time_predict
from ToolBox.shortest_path import print_shortest_path
from ToolBox.route_efficiency import route_efficiency_analysis
from ToolBox.Interactive_Site_Map import add_map
from ToolBox.Bus_Stop_Utilization_Analysis import print_underutilized_stops, print_recommended_stops

# Load data
stops_df = load_stops_df("urban_transport_network_stops.csv")
routes_df = load_routes_df("urban_transport_network_routes.csv")

class UrbanTransportApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Urban Transportation Analysis")

        self.setup_ui()

    def setup_ui(self):
        # Start node input
        self.start_node_label = ttk.Label(self, text="Start Node:")
        self.start_node_label.pack(pady=(10, 0))
        self.start_node_entry = ttk.Entry(self)
        self.start_node_entry.pack(pady=(0, 10))

        # End node input
        self.end_node_label = ttk.Label(self, text="End Node:")
        self.end_node_label.pack(pady=(10, 0))
        self.end_node_entry = ttk.Entry(self)
        self.end_node_entry.pack(pady=(0, 10))

        # Button to plot transport network
        ttk.Button(self, text="Plot Transport Network", command=self.plot_transport_network).pack(pady=5)

        # Button to find highest centrality
        ttk.Button(self, text="Find Highest Centrality", command=self.find_highest_centrality).pack(pady=5)

        # Button to find routes
        ttk.Button(self, text="Find Routes", command=self.find_routes).pack(pady=5)

        # Button to predict time
        ttk.Button(self, text="Predict Time", command=self.predict_time).pack(pady=5)

        # Button to find shortest path
        ttk.Button(self, text="Find Shortest Path", command=self.find_shortest_path).pack(pady=5)

        # Button to analyze route efficiency
        ttk.Button(self, text="Analyze Route Efficiency", command=self.analyze_route_efficiency).pack(pady=5)

        # Button to show interactive site map
        ttk.Button(self, text="Show Interactive Site Map", command=self.show_interactive_site_map).pack(pady=5)

        # Button to analyze bus stop utilization
        ttk.Button(self, text="Analyze Bus Stop Utilization", command=self.analyze_bus_stop_utilization).pack(pady=5)

    def plot_transport_network(self):
        try:
            start_node = int(self.start_node_entry.get())
            end_node = int(self.end_node_entry.get())
            my_graph = create_graph(stops_df, routes_df)
            plot_transport_network(my_graph)
            messagebox.showinfo("Plot Transport Network", f"Plotted transport network from node {start_node} to {end_node}.")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid node IDs.")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def find_highest_centrality(self):
        try:
            result = print_highest_cretrality()
            messagebox.showinfo("Find Highest Centrality", f"Highest centrality nodes: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def find_routes(self):
        try:
            result = create_routes_graph()
            messagebox.showinfo("Find Routes", f"Created route graph: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def predict_time(self):
        try:
            result = print_time_predict()
            messagebox.showinfo("Predict Time", f"Predicted time: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def find_shortest_path(self):
        try:
            result = print_shortest_path()
            messagebox.showinfo("Find Shortest Path", f"Shortest path: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def analyze_route_efficiency(self):
        try:
            result = route_efficiency_analysis()
            messagebox.showinfo("Analyze Route Efficiency", f"Route efficiency analysis: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def show_interactive_site_map(self):
        try:
            result = add_map()
            messagebox.showinfo("Show Interactive Site Map", f"Interactive site map added: {result}")
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

    def analyze_bus_stop_utilization(self):
        try:
            underutilized_stops = print_underutilized_stops()
            recommended_stops = print_recommended_stops()
            result = f"Underutilized stops: {underutilized_stops}\nRecommended stops: {recommended_stops}"
            messagebox.showinfo("Analyze Bus Stop Utilization", result)
        except Exception as e:
            messagebox.showerror("Error", f"Error occurred: {str(e)}")

if __name__ == "__main__":
    app = UrbanTransportApp()
    app.mainloop()
