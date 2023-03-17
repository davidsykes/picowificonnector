from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
sys.path.append('../src')
from pico_access_point import PicoAccessPoint
import usocket

hostName = "localhost"
serverPort = 8080

class MockProgressIndicator:
    def set_progress(self, value):
        pass

class MockPicoWrapper:
    def log(self, l):
        print(l)

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/form':
            ap = PicoAccessPoint(MockPicoWrapper(), MockProgressIndicator())
            usocket.socket.http_requests = [b'/',b'reset']
            ap.launch()
            self.wfile.write(bytes(usocket.Connection.http_response, "utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><p>Request:", "utf-8"))
            self.wfile.write(bytes(self.path, "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")