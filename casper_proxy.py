import sys
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.request
import urllib.error
from dotenv import load_dotenv
from pathlib import Path

# Load env variables from the main server's .env file
server_env_path = Path(__file__).parent.parent.parent / "undesirables-x402-server" / ".env"
load_dotenv(server_env_path)

API_KEY = os.getenv("CSPR_API_KEY")
TARGET_URL = "https://node.testnet.cspr.cloud/rpc"

class ProxyHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        req = urllib.request.Request(TARGET_URL, data=body, method='POST')
        req.add_header('Content-Type', 'application/json')
        req.add_header('Authorization', API_KEY)
        
        try:
            with urllib.request.urlopen(req) as response:
                resp_body = response.read()
                self.send_response(response.status)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(resp_body)
        except urllib.error.HTTPError as e:
            self.send_response(e.code)
            self.end_headers()
            self.wfile.write(e.read())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode('utf-8'))

    def log_message(self, format, *args):
        # Suppress noisy HTTP logs
        return

if __name__ == "__main__":
    server = HTTPServer(('127.0.0.1', 7777), ProxyHandler)
    print("Local Casper RPC Proxy listening on http://127.0.0.1:7777")
    server.serve_forever()
