import os
import json
import unittest
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

from forest_tracker import (
    add_hours,
    show_hours,
    total_hours,
    fetch_forest_hours,
    DATA_FILE,
)

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

    def test_fetch_forest_hours(self):
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                payload = {"date": "2023-07-23", "hours": 2}
                body = json.dumps(payload).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format, *args):  # pragma: no cover
                return

        server = HTTPServer(("localhost", 0), Handler)
        thread = Thread(target=server.serve_forever)
        thread.daemon = True
        thread.start()

        url = f"http://{server.server_address[0]}:{server.server_address[1]}"
        date_str, hours = fetch_forest_hours(url)
        add_hours('carol', date_str, hours)
        data = show_hours('carol')
        self.assertEqual(data['2023-07-23'], 2)

        server.shutdown()
        server.server_close()
        thread.join()

if __name__ == '__main__':
    unittest.main()
