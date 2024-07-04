import unittest
import os
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

import sys
# Get the directory of the current script file(获取当前脚本文件的目录)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Add the parent directory (project root directory) to the system path 将上级目录（项目根目录）添加到系统路径中
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from ToolBox.GUI import TrafficNetworkGUI  # Adjust import as per your project structure

class TestTrafficNetworkGUI(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Setup method to initialize QApplication once for all tests."""
        cls.app = QApplication([])

    def setUp(self):
        """Setup method to initialize TrafficNetworkGUI for each test."""
        self.gui = TrafficNetworkGUI()
        self.gui.show()

    def tearDown(self):
        """Teardown method to clean up after each test."""
        self.gui.close()
        del self.gui

    @classmethod
    def tearDownClass(cls):
        """Teardown method to clean up QApplication after all tests."""
        cls.app.quit()

    def test_add_stop(self):
        """Test adding a stop."""
        initial_stops_count = len(self.gui.stops)
        self.gui.add_stop()
        self.assertEqual(len(self.gui.stops), initial_stops_count + 1)

    def test_remove_stop(self):
        """Test removing a stop."""
        initial_stops_count = len(self.gui.stops)
        if initial_stops_count > 0:
            self.gui.remove_stop()
            self.assertEqual(len(self.gui.stops), initial_stops_count - 1)
    
    def test_undo_remove_stop(self):
        """Test undoing the removal of a stop."""
        initial_stops_count = len(self.gui.stops)
        if initial_stops_count > 0:
            self.gui.remove_stop()
            self.gui.undo_remove()
            self.assertEqual(len(self.gui.stops), initial_stops_count)

    def test_find_and_draw_routes(self):
        """Test finding and drawing routes."""
        self.gui.find_and_draw_routes()
        self.assertTrue(self.gui.route_paths)  # Assert that routes are found and stored

    def test_draw_shortest_route(self):
        """Test drawing the shortest route."""
        self.gui.draw_shortest_route()
        self.assertTrue(self.gui.route_paths)  # Assert that shortest route is found and drawn

    def test_map_display(self):
        """Test if the map is displayed."""
        self.assertIsInstance(self.gui.webView, QWebEngineView)
        expected_url = QUrl.fromLocalFile(os.path.abspath('map.html'))
        current_url = self.gui.webView.url()
        # Normalize paths for comparison (convert to lower case for case-insensitive comparison on Windows)
        self.assertEqual(current_url.toLocalFile().lower(), expected_url.toLocalFile().lower())

if __name__ == "__main__":
    unittest.main()
