from enum import Enum, auto
import csv

class ZoneType(Enum):
    RESIDENTIAL = auto()
    COMMERCIAL = auto()
    INDUSTRIAL = auto()
    MIXED = auto()

class TransportStop:
    def __init__(self, stop_id, name, latitude, longitude, zone_type):
        self.stop_id = stop_id
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        if isinstance(zone_type, ZoneType):
            self.zone_type = zone_type
        else:
            raise ValueError("Invalid zone_type value")

    def __str__(self):
        return f"Stop {self.stop_id}: {self.name} ({self.latitude}, {self.longitude}), Zone: {self.zone_type.name}"

    def __repr__(self):
        return f"TransportStop(stop_id={self.stop_id}, name='{self.name}', latitude={self.latitude}, longitude={self.longitude}, zone_type={self.zone_type})"

    def __lt__(self, other):
        return self.stop_id < other.stop_id
    
def read_transport_stops_from_csv(filename):
    stops = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                start_stop_id = int(row['start_stop_id'])
                end_stop_id = row['end_stop_id']  
                distance = float(row['distance'])  
                
                stops.append(stop)
            except ValueError:
                print(f"Error processing row: {row}")
    return stops

# Example usage:
if __name__ == "__main__":
    csv_filename = "urban_transport_network_routes.csv"
    transport_stops = read_transport_stops_from_csv(csv_filename)
    for stop in transport_stops:
        print(stop)