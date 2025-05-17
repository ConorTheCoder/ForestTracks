import os
import json
import unittest
from forest_tracker import add_hours, show_hours, total_hours, DATA_FILE

class TrackerTestCase(unittest.TestCase):
    def setUp(self):
        # Ensure a clean data file
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def tearDown(self):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)

    def test_add_and_show_hours(self):
        add_hours('alice', '2023-07-21', 2)
        add_hours('alice', '2023-07-21', 1)
        data = show_hours('alice')
        self.assertEqual(data['2023-07-21'], 3)

    def test_total_hours(self):
        add_hours('bob', '2023-07-21', 2)
        add_hours('bob', '2023-07-22', 4)
        self.assertEqual(total_hours('bob'), 6)

if __name__ == '__main__':
    unittest.main()
