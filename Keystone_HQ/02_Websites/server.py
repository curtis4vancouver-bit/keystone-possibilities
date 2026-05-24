import http.server
import socketserver
import webbrowser

PORT = 8080
DIRECTORY = "."

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"[Keystone Server] Serving B2C Recomposition Web at http://localhost:{PORT}")
    webbrowser.open(f"http://localhost:{PORT}/index.html")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[Keystone Server] Server stopped.")
