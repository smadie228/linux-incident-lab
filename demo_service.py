"""Локальный HTTP-сервис: healthy, error, slow."""
import argparse
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer


def create_handler(mode):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path != "/health":
                status, body = 404, b"Not found\n"
            elif mode == "error":
                status, body = 503, b"Service unavailable\n"
            else:
                if mode == "slow":
                    time.sleep(4)
                status, body = 200, b"OK\n"

            self.send_response(status)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            try:
                self.wfile.write(body)
            except BrokenPipeError:
                pass  # клиент мог отключиться по таймауту

    return Handler


def main():
    parser = argparse.ArgumentParser(description="Учебный сервис с ошибками")
    parser.add_argument("--mode", choices=("healthy", "error", "slow"),
                        default="healthy")
    parser.add_argument("--port", type=int, default=8080)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("Неверный порт")

    server = ThreadingHTTPServer(("127.0.0.1", args.port),
                                 create_handler(args.mode))
    print(f"Mode={args.mode}, http://127.0.0.1:{args.port}/health")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
