import http.server, os, socketserver

PORT = int(os.environ.get("PORT", 8080))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"StampForge running on port {PORT}")
    httpd.serve_forever()
