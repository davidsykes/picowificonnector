import sys
sys.path.append('../src')
from network_initialiser import NetworkInitialiser

class MockPicoWrapper:
    def __init__(self):
        self.password_file = None
        self.logs = []
    def read_file_data(self, file_name):
        if file_name == 'ssid.txt':
            return self.password_file
    def log(self, log):
        self.logs.append(log)

class MockAccessPoint:
    def __init__(self):
        self.access_point_launched = False
    def launch(self):
        self.access_point_launched = True

class MockWiFiConnection:
    def __init__(self):
        self.mock_wifi_connected = False
    def connect_wifi(self, ssid, password):
        if ssid == 'ssid' and password == '12345678':
            self.mock_wifi_connected = True
        return self.mock_wifi_connected
    
class MockProgress:
    def set_progress(self, message):
        pass

class TestNetworkInitialiser:
    def setup_method(self, test_method):
        self.mock_access_point = MockAccessPoint()
        self.mock_wifi_connection = MockWiFiConnection()
        self.mock_pico_wrapper = MockPicoWrapper()
        self.mock_progress = MockProgress()
        self.initialiser = NetworkInitialiser(self.mock_pico_wrapper, self.mock_progress, self.mock_wifi_connection, self.mock_access_point)

    def test_if_the_password_file_is_not_found_the_access_point_is_launched(self):
        self.mock_pico_wrapper.password_file = None

        self.initialiser.initialise()

        assert(self.mock_access_point.access_point_launched == True)
        assert(self.mock_pico_wrapper.logs == ['The credentials file was not found.'])

    def test_if_the_file_is_found_the_wifi_connection_is_initialised(self):
        self.mock_pico_wrapper.password_file = "ssid\n12345678"

        self.initialiser.initialise()

        assert(self.mock_wifi_connection.mock_wifi_connected == True)
        assert(self.mock_pico_wrapper.logs == ['Attempting to connect to ssid-12345678','Connected.'])

    def test_if_the_network_intialisation_fails_the_access_point_is_launched(self):
        self.mock_pico_wrapper.password_file = "ssid\nxxx"

        self.initialiser.initialise()

        assert(self.mock_access_point.access_point_launched == True)
        assert(self.mock_pico_wrapper.logs == ['Attempting to connect to ssid-xxx','Connection failed.'])
