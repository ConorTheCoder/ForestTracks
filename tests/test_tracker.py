import os
import json
import unittest
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
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
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                body = json.dumps({'date': '2023-07-23', 'hours': 2})
                self.wfile.write(body.encode())

        server = HTTPServer(('localhost', 0), Handler)

        def run_server():
            with server:
                server.serve_forever()

        thread = Thread(target=run_server, daemon=True)
        thread.start()
        url = f'http://{server.server_address[0]}:{server.server_address[1]}'
        date_str, hours = fetch_forest_hours(url)
        self.assertEqual(date_str, '2023-07-23')
        self.assertEqual(hours, 2)
        server.shutdown()

if __name__ == '__main__':
    unittest.main()
