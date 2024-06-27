import csv
import os
import sys

# Get the current script file's directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root) to the system path
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.transportstop import TransportStop
from ToolBox.read_csv import read_stops_from_csv

class UrbanTransportNetwork:
    def __init__(self):
        self.stops = {}  # Dictionary to store stops (stop_id: Stop object)
        self.routes = []  # List to store routes (list of stop_ids)

    def add_stop(self, stop_id, name, latitude, longitude, zone_type):
        # Create a new Stop object and add it to the stops dictionary
        stop = TransportStop(stop_id, name, latitude, longitude, zone_type)
        self.stops[stop_id] = stop

if __name__ == "__main__":
    network = UrbanTransportNetwork()

    stops_data = read_stops_from_csv("urban_transport_network_stops.csv")
    for stop_data in stops_data:
        network.add_stop(stop_data.stop_id, stop_data.name, stop_data.latitude, stop_data.longitude, stop_data.zone_type)


