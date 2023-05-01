import sys
import network
import usocket
sys.path.append('../src')
from pico_access_point import PicoAccessPoint
from constants import PROGRAM_OPTIONS_FILE
from access_point_option import AccessPointOption
from access_point_options import AccessPointOptions

class MockPicoWrapper:
    def __init__(self):
        self.files = {}
    def write_parameters_to_file(self, path, parameters):
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

class MockAccessPointFormCreator:
    def create_form(self, options):
        return 'access point form ' + options[0].text

class TestPicoAccessPoint:
    def setup_method(self, test_method):
        di = {}
        di['ProgressIndicator'] = MockProgress()
        di['PicoWrapper'] = MockPicoWrapper()
        di['UrlParametersExtractor'] = MockParametersExtractor()
        di['AccessPointFormCreator'] = MockAccessPointFormCreator()
        self.pico_wrapper = di['PicoWrapper']
        self.mock_parameters_extractor = di['UrlParametersExtractor']
        access_point_options = AccessPointOptions('ssid', 'password', [AccessPointOption('option1', 'option 1')])
        self.ap = PicoAccessPoint(di, access_point_options)

    def test_an_access_point_is_initialised(self):
        usocket.socket.http_requests = ['reset']
        self.ap.launch()

        assert(network.WLAN.type == network.AP_IF)
        assert(network.WLAN.essid == 'ssid')
        assert(network.WLAN.password == 'password')

    def test_a_simple_request_gets_the_main_form(self):
        usocket.socket.http_requests = ['request', 'reset']
        self.ap.launch()
        
        assert('access point form' in usocket.Connection.http_response)
        assert('option 1' in usocket.Connection.http_response)

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