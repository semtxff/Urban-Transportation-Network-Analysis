import unittest
import pandas as pd
import numpy as np
from io import StringIO
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.Bus_Stop_Utilization_Analysis import analyze_stop_utilization, recommend_new_stops

class test_Bus_Stop_Utilization_Analysis(unittest.TestCase):

    def setUp(self):
        data = StringIO("""
        stop_id,passenger_count
        1,50
        2,120
        3,30
        4,90
        5,60
        """)
        self.stops_df = pd.read_csv(data)
        self.stops_df.columns = self.stops_df.columns.str.strip()

    def test_analyze_stop_utilization(self):
        underutilized_stops = analyze_stop_utilization(self.stops_df)
        expected_underutilized = pd.DataFrame({
            'stop_id': [1, 3, 5],
            'passenger_count': [50, 30, 60]
        })
        pd.testing.assert_frame_equal(underutilized_stops.reset_index(drop=True), expected_underutilized)

    def test_recommend_new_stops(self):
        recommended_stops = recommend_new_stops(self.stops_df)
        pd.testing.assert_frame_equal(recommended_stops, self.stops_df)

if __name__ == '__main__':
    unittest.main()