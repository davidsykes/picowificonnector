import sys
import network
import usocket
sys.path.append('../src')
from pico_access_point import PicoAccessPoint
from constants import PROGRAM_OPTIONS_FILE

class MockPicoWrapper:
    def __init__(self):
        self.files = {}
    def log(self, log):
        pass        
    def store_parameters(self, path, parameters):
        params = ''
        for key, value in parameters.items():
            params = params + ''.join([key, '=', value, '\n'])
        self.files[path] = params
    def reset(self):
        self.pico_was_reset = True
    def print(self, p):
        pass

class MockProgress:
    def __init__(self):
        self.value = 0
    def set_progress(self, value):
        self.value = value

class MockParametersExtractor:
    def __init__(self):
        self.parameters = {'ssid': 'the_ssid', 'password': 'the_password'}
    def extract_parameters(self, request):
        if request == 'parameters':
            return self.parameters
        return {}

class TestPicoAccessPoint:
    def setup_method(self, test_method):
        self.pico_wrapper = MockPicoWrapper()
        self.mock_progress = MockProgress()
        self.mock_parameters_extractor = MockParametersExtractor()
        self.ap = PicoAccessPoint('PICO', '12345678', self.pico_wrapper, self.mock_progress, self.mock_parameters_extractor)

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

    def test_simple_parameters_are_stored(self):
        usocket.socket.http_requests = ['parameters', 'reset']
        self.ap.launch()
    
        assert(self.pico_wrapper.files[PROGRAM_OPTIONS_FILE] == "ssid=the_ssid\npassword=the_password\n")
        assert('OK' in usocket.Connection.http_response)

    def test_when_parameters_are_supplied_the_pico_is_reset(self):
        usocket.socket.http_requests = ['parameters', 'reset']
        self.ap.launch()
    
        assert(self.pico_wrapper.pico_was_reset == True)

    def test_when_parameters_are_supplied_they_are_acknowledged(self):
        usocket.socket.http_requests = ['parameters', 'reset']
        self.ap.launch()
        
        assert('<head><title>Parameters Accepted</title></head>' in usocket.Connection.http_response)

    def test_when_details_are_requested_the_details_are_displayed(self):
        usocket.socket.http_requests = ['parameters', 'reset']
        self.mock_parameters_extractor.parameters['show'] = 'y'
        self.ap.launch()
    
        assert('the_ssid' in usocket.Connection.http_response)
        assert('the_password' in usocket.Connection.http_response)

    def test_when_details_are_not_requested_the_details_are_not_displayed(self):
        usocket.socket.http_requests = ['parameters', 'reset']
        self.ap.launch()
    
        assert('OK' in usocket.Connection.http_response)
        assert('the_ssid' not in usocket.Connection.http_response)
        assert('the_password' not in usocket.Connection.http_response)