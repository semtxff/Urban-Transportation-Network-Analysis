import pandas as pd
from enum import Enum, auto

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

# Read data from a CSV file
def read_stops_from_csv(file_path):
    try:
        data = pd.read_csv(file_path)
        stops = []
        for _, row in data.iterrows():
            stop = TransportStop(
                stop_id=row['stop_id'],
                name=row['name'],
                latitude=row['latitude'],
                longitude=row['longitude'],
                zone_type=ZoneType[row['zone_type'].upper()]  # Convert to uppercase and match enum value
            )
            stops.append(stop)
        return stops
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return []

# File path
csv_file_path = r"C:\Users\18116\Desktop\AAD\file\urban_transport_network_stops.csv"
transport_stops = read_stops_from_csv(csv_file_path)

# Print data
for stop in transport_stops:
    print(stop)

