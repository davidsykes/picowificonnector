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
    def reset(self):
        self.pico_was_reset = True
    def print(self, p):
        pass

class MockProgress:
    def __init__(self):
        self.value = 0
    def set_progress(self, value):
        self.value = value

class MockCredentialsExtractor:
    def __init__(self):
        self.results = (None,None,None)
    def extract_credentials(self, request):
        return self.results

class TestPicoAccessPoint:
    def setup_method(self, test_method):
        self.pico_wrapper = MockPicoWrapper()
        self.mock_progress = MockProgress()
        self.mock_credentials_extractor = MockCredentialsExtractor()
        self.ap = PicoAccessPoint(self.pico_wrapper, self.mock_progress, self.mock_credentials_extractor)

    def test_an_access_point_is_initialised(self):
        usocket.socket.http_requests = ['reset']
        self.ap.launch()

        assert(network.WLAN.type == network.AP_IF)
        assert(network.WLAN.essid == 'PICO')
        assert(network.WLAN.password == '12345678')

    def test_a_simple_request_gets_the_main_form(self):
        usocket.socket.http_requests = ['request', 'reset']
        self.ap.launch()
        
        assert('<form style' in usocket.Connection.http_response)
        assert('<head><title>SSID Input</title></head>' in usocket.Connection.http_response)

    def test_simple_credentials_are_stored(self):
        usocket.socket.http_requests = ['credentials', 'reset']
        self.mock_credentials_extractor.results = ('the_ssid','the_password',False)
        self.ap.launch()
    
        assert(self.pico_wrapper.files['ssid.txt'] == "the_ssid\nthe_password")
        assert('OK' in usocket.Connection.http_response)

    def test_when_credentials_are_supplied_the_pico_is_reset(self):
        usocket.socket.http_requests = ['credentials', 'reset']
        self.mock_credentials_extractor.results = ('the_ssid','the_password',False)
        self.ap.launch()
    
        assert(self.pico_wrapper.pico_was_reset == True)

    def test_when_credentials_are_supplied_they_are_acknowledged(self):
        usocket.socket.http_requests = ['credentials', 'reset']
        self.mock_credentials_extractor.results = ('the_ssid','the_password',False)
        self.ap.launch()
        
        assert('<head><title>Credentials Accepted</title></head>' in usocket.Connection.http_response)

    def test_when_details_are_requested_the_details_are_displayed(self):
        usocket.socket.http_requests = ['credentials', 'reset']
        self.mock_credentials_extractor.results = ('the_ssid','the_password',True)
        self.ap.launch()
    
        assert('the_ssid' in usocket.Connection.http_response)
        assert('the_password' in usocket.Connection.http_response)

    def test_when_details_are_not_requested_the_details_are_not_displayed(self):
        usocket.socket.http_requests = ['credentials', 'reset']
        self.mock_credentials_extractor.results = ('the_ssid','the_password',False)
        self.ap.launch()
    
        assert('OK' in usocket.Connection.http_response)
        assert('the_ssid' not in usocket.Connection.http_response)
        assert('the_password' not in usocket.Connection.http_response)