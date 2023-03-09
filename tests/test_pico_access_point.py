import sys
import network
import usocket
sys.path.append('../src')
from pico_access_point import PicoAccessPoint

class MockPicoWrapper:
    def __init__(self):
        self.files = {}
    def log(self, log):
        pass        
    def store_credentials(self, path, ssid, password):
        self.files[path] = ssid + "\n" + password

class MockProgress:
    def __init__(self):
        self.value = 0
    def set_progress(self, value):
        self.value = value

class TestPicoAccessPoint:
    def setup_method(self, test_method):
        self.pico_wrapper = MockPicoWrapper()
        self.mock_progress = MockProgress()
        self.ap = PicoAccessPoint(self.pico_wrapper, self.mock_progress)

    def test_an_access_point_is_initialised(self):
        usocket.socket.http_requests = ['reset']
        self.ap.launch()

        assert(network.WLAN.type == network.AP_IF)
        assert(network.WLAN.essid == 'PICO')
        assert(network.WLAN.password == '12345678')

    def test_a_simple_request_gets_the_main_form(self):
        usocket.socket.http_requests = ['/', 'reset']
        self.ap.launch()
        
        assert('<form style' in usocket.Connection.http_response)

    def test_simple_credentials_are_stored(self):
        usocket.socket.http_requests = ['GET /?ssid=the_ssid&password=the_password&submit=Submit HTTP/1.1\r\n', 'reset']
        self.ap.launch()
    
        assert(self.pico_wrapper.files['ssid.txt'] == "the_ssid\nthe_password")
        assert('OK' in usocket.Connection.http_response)