from http.server import BaseHTTPRequestHandler, HTTPServer
import sys
sys.path.append('../src')
from access_point_option import AccessPointOption
from access_point_options import AccessPointOptions
from pico_access_point import PicoAccessPoint
from access_point_form_creator import AccessPointFormCreator
import usocket

hostName = "localhost"
serverPort = 8080

class MockProgressIndicator:
    def set_progress(self, message):
        pass

class MockPicoWrapper:
    def log(self, l):
        print(l)
    def write_parameters_to_file(self, path, parameters):
        print('Write parameters to', path)
        print(parameters)
    def reset(self):
        pass
    def print(self, p):
        pass

class MockUrlParametersExtractor:
    def __init__(self, ssid, password, show):
        self.parameters = {}
        if ssid is not None:
            self.parameters['ssid'] = ssid
        if password is not None:
            self.parameters['password'] = password
        if show:
            self.parameters['show'] = show
    def extract_parameters(self, request):
        return self.parameters

def set_up_url_parameters_to_show_input_form():
    return MockUrlParametersExtractor(None, None, None)

def set_up_url_parameters_with_ssid_and_password(show):
    return MockUrlParametersExtractor('ssid', 'password', show)

def create_access_point(url_parameters_to_extract):
    di = { 'PicoWrapper': MockPicoWrapper(), 'ProgressIndicator' : MockProgressIndicator(), 'UrlParametersExtractor' : url_parameters_to_extract, 'AccessPointFormCreator' : AccessPointFormCreator() }
    option = AccessPointOption('option1', 'the option')
    ap = PicoAccessPoint(di, AccessPointOptions('the ssid', 'the password', [option]))
    return ap

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/ssidinput':
            pe = set_up_url_parameters_to_show_input_form()
            ap = create_access_point(pe)
            usocket.socket.http_requests = [b'/',b'reset']
            ap.launch()
            self.wfile.write(bytes(usocket.Connection.http_response, "utf-8"))
        elif self.path == '/ssidwithoutdetails':
            pe = set_up_url_parameters_with_ssid_and_password(False)
            ap = create_access_point(pe)
            usocket.socket.http_requests = [b'GET /etc',b'reset']
            ap.launch()
            self.wfile.write(bytes(usocket.Connection.http_response, "utf-8"))
        elif self.path == '/ssidwithdetails':
            pe = set_up_url_parameters_with_ssid_and_password(True)
            ap = create_access_point(pe)
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