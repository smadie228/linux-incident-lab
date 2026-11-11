"""Два простых теста без внешних библиотек."""
import sys
import threading
import unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import urlopen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from demo_service import create_handler


class DemoTests(unittest.TestCase):
    def check_mode(self, mode, expected):
        server = ThreadingHTTPServer(("127.0.0.1", 0), create_handler(mode))
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            url = f"http://127.0.0.1:{server.server_port}/health"
            try:
                with urlopen(url, timeout=2) as response:
                    status = response.status
            except HTTPError as exc:
                status = exc.code
            self.assertEqual(status, expected)
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)

    def test_healthy(self):
        self.check_mode("healthy", 200)

    def test_error(self):
        self.check_mode("error", 503)


if __name__ == "__main__":
    unittest.main()
