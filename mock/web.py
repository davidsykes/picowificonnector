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
    def store_credentials(self, path, ssid, password):
        pass
    def reset(self):
        pass
    def print(self, p):
        pass

class MockCredentialsExtractor:
    def __init__(self, ssid, password, show):
        self.return_value = (ssid, password, show)
    def extract_credentials(self, request):
        return self.return_value

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ssidinput':
            ap = PicoAccessPoint(MockPicoWrapper(), MockProgressIndicator(), MockCredentialsExtractor(None,None,None))
            usocket.socket.http_requests = [b'/',b'reset']
            ap.launch()
            self.wfile.write(bytes(usocket.Connection.http_response, "utf-8"))
        elif self.path == '/ssidwithoutdetails':
            ap = PicoAccessPoint(MockPicoWrapper(), MockProgressIndicator(), MockCredentialsExtractor('ssid','pswd',False))
            usocket.socket.http_requests = [b'GET /etc',b'reset']
            ap.launch()
            self.wfile.write(bytes(usocket.Connection.http_response, "utf-8"))
        elif self.path == '/ssidwithdetails':
            ap = PicoAccessPoint(MockPicoWrapper(), MockProgressIndicator(), MockCredentialsExtractor('ssid','pswd',True))
            usocket.socket.http_requests = [b'GET /etc',b'reset']
            ap.launch()
            self.wfile.write(bytes(usocket.Connection.http_response, "utf-8"))
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes("<html><body><p>Request:", "utf-8"))
            self.wfile.write(bytes(self.path, "utf-8"))
            self.wfile.write(bytes('<br><a href="ssidinput">ssid input</a>', "utf-8"))
            self.wfile.write(bytes('<br><a href="ssidwithoutdetails">ssid without details</a>', "utf-8"))
            self.wfile.write(bytes('<br><a href="ssidwithdetails">ssid with details</a>', "utf-8"))
            self.wfile.write(bytes('</body></html>', "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")