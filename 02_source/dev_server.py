import http.server
import socketserver
import os
import sys

PORT = 8000

# 🌟 Load environment variables from .env file if it exists (for local convenience)
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../.env')
if os.path.exists(env_path):
    with open(env_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, val = line.split('=', 1)
                val = val.strip().strip('"').strip("'")
                os.environ[key.strip()] = val

class DevServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == '/api/coach':
            # Dynamically import and delegate handling to api/coach.py's handler class method
            parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)
            from api.coach import handler as CoachHandler
            CoachHandler.do_POST(self)
        else:
            super().do_POST()
            
    def do_GET(self):
        if self.path == '/api/news':
            parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)
            from api.news import handler as NewsHandler
            NewsHandler.do_GET(self)
        else:
            super().do_GET()

    def do_OPTIONS(self):
        if self.path in ('/api/coach', '/api/news'):
            parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
            if parent_dir not in sys.path:
                sys.path.append(parent_dir)
            if self.path == '/api/coach':
                from api.coach import handler as CoachHandler
                CoachHandler.do_OPTIONS(self)
            else:
                from api.news import handler as NewsHandler
                NewsHandler.do_OPTIONS(self)
        else:
            super().do_OPTIONS()

print(f"==========================================================")
print(f" [START] AI Career Oasis Local Dev Server starting...")
print(f" Running at: http://localhost:{PORT}")
print(f" Press Ctrl+C to stop.")
print(f" Make sure to set GEMINI_API_KEY environment variable!")
print(f"==========================================================")

# Change working directory to ensure correct static file serving (parent directory)
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

with socketserver.ThreadingTCPServer(("", PORT), DevServerHandler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping dev server.")
        httpd.server_close()
