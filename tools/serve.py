"""Dev server for the Wall Jewels site with caching disabled.

The plain `python -m http.server` sends no Cache-Control headers, so browsers
heuristically cache pages and keep showing stale builds. This wrapper serves
the same directory but tells the browser to always revalidate.

Usage:  python tools/serve.py [port]
"""
import http.server
import functools
import os
import sys

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5178


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, must-revalidate")
        super().end_headers()

    def log_message(self, fmt, *args):  # quieter logs
        pass


if __name__ == "__main__":
    handler = functools.partial(NoCacheHandler, directory=SITE)
    with http.server.ThreadingHTTPServer(("", PORT), handler) as httpd:
        print(f"serving {SITE} on http://localhost:{PORT} (no-cache)")
        httpd.serve_forever()
