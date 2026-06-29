#!/usr/bin/env python3
"""
Keystone Cognitive Substrate Control Console Server.
Launches a standard lightweight Python HTTP server to host the interactive control panel.
"""

import sys
import http.server
import socketserver
import webbrowser
from pathlib import Path

PORT = 8000
DIRECTORY = Path(__file__).parent.resolve()


class SafeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DIRECTORY), **kwargs)

    def log_message(self, format, *args):
        # Format custom server logs cleanly in stdout
        sys.stdout.write(f"[Server Log] {format % args}\n")


def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), SafeHTTPRequestHandler) as httpd:
        print("=" * 80)
        print("   🧠 KEYSTONE COGNITIVE SUBSTRATE CONTROL DASHBOARD SERVER (v2.1) 🧠   ")
        print("=" * 80)
        print(f"Local Server Root:  {DIRECTORY}")
        print(f"Server Port:        {PORT}")
        print(f"Dashboard URL:      http://localhost:{PORT}/index.html")
        print("-" * 80)
        print("[Status] Server is listening... Press Ctrl+C to terminate.")
        print("=" * 80)
        
        # Auto-open the user's browser
        try:
            webbrowser.open(f"http://localhost:{PORT}/index.html")
        except Exception:
            pass

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[Status] Server terminated by user. Exiting.")
            sys.exit(0)


if __name__ == "__main__":
    start_server()
