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

    def __repr__(self):
        return f"TransportStop(stop_id={self.stop_id}, name='{self.name}', latitude={self.latitude}, longitude={self.longitude}, zone_type={self.zone_type})"

    def __lt__(self, other):
        return self.stop_id < other.stop_id
    
def read_stops_from_csv(file_path):
    try:
        import pandas as pd
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
