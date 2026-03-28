#!/usr/bin/env python3
"""
Local static server for this site. Uses a non-default port and no-cache headers
so edits show up immediately without fighting port collisions or browser cache.
"""
from __future__ import annotations

import http.server
import os
import socketserver

PORT = int(os.environ.get("PORT", "8765"))
ROOT = os.path.dirname(os.path.abspath(__file__))


class DevHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        super().end_headers()


if __name__ == "__main__":
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), DevHandler) as httpd:
        print(f"Serving HTTP on http://127.0.0.1:{PORT}/ (dev, no-cache)", flush=True)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.", flush=True)
