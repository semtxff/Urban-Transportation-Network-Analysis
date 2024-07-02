import unittest
import pandas as pd
from io import StringIO
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.Peak_Hours_Traffic_Analysis import peak_hour_traffic_analysis, optimize_peak_hour_routes

class test_Peak_Hours_Traffic_Analysis(unittest.TestCase):

    def setUp(self):
        stops_data = """stop_id,stop_name
                        1,Stop A
                        2,Stop B"""
        routes_data = """route_id,distance
                         1,10
                         2,20"""
        self.stops_df = pd.read_csv(StringIO(stops_data))
        self.routes_df = pd.read_csv(StringIO(routes_data))

    def test_peak_hour_traffic_analysis(self):
        expected_congestion_factor = 1.5
        expected_peak_hour_distance = self.routes_df['distance'] * expected_congestion_factor
        result_df = peak_hour_traffic_analysis(self.routes_df.copy())

        pd.testing.assert_series_equal(result_df['peak_hour_distance'], expected_peak_hour_distance, check_names=False)

    def test_optimize_peak_hour_routes(self):
        optimized_df = optimize_peak_hour_routes(self.routes_df.copy())
        pd.testing.assert_frame_equal(optimized_df, self.routes_df)

if __name__ == '__main__':
    unittest.main()