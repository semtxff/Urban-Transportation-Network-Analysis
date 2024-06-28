import unittest
import csv
import os
import sys


current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.transportstop import TransportStop
from ToolBox.transportstop import ZoneType
from ToolBox.transportstop import read_transport_stops_from_csv

class test_transportstop(unittest.TestCase):
    def test_stop_creation(self):
        stop = TransportStop(stop_id=1, name="Sample Stop", latitude=40.7128, longitude=-74.0060, zone_type=ZoneType.RESIDENTIAL)
        self.assertEqual(stop.stop_id, 1)
        self.assertEqual(stop.name, "Sample Stop")
        self.assertEqual(stop.latitude, 40.7128)
        self.assertEqual(stop.longitude, -74.0060)
        self.assertEqual(stop.zone_type, ZoneType.RESIDENTIAL)

    def test_invalid_zone_type(self):
        with self.assertRaises(ValueError):
            TransportStop(stop_id=2, name="Invalid Stop", latitude=35.6895, longitude=139.6917, zone_type="INVALID")

def read_transport_stops_from_csv(filename):
    stops = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                start_stop_id = int(row['start_stop_id'])
                end_stop_id = int(row['end_stop_id'])
                distance = float(row['distance'])

                stop = TransportStop(stop_id=start_stop_id, name=row['name'], latitude=row['latitude'], longitude=row['longitude'], zone_type=row['zone_type'])
                stops.append(stop)
            except ValueError:
                print(f"Error processing row: {row}")
    return stops


if __name__ == "__main__":
    unittest.main()