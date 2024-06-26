import sys
sys.path.append('../src')
from network_initialiser import NetworkInitialiser
from constants import RESET_PIN, PROGRAM_OPTIONS_FILE

class MockPin:
    def __init__(self, value):
        self._value = value
    def value(self):
        return self._value

class MockPicoWrapper:
    def __init__(self):
        self.logs = []
        self.deleted_file = None
        self.reset_pin_value = True
    def log(self, log):
        self.logs.append(log)
    def create_input_pin_with_pullup(self, pin_number):
        if (pin_number == RESET_PIN):
            return MockPin(self.reset_pin_value)
    def delete_file(self, file_name):
        self.deleted_file = file_name
    
class MockProgress:
    timer_has_been_deinitialised = False
    def set_progress(self, message):
        pass
    def stop(self):
        self.timer_has_been_deinitialised = True

class MockWiFiConnection:
    def __init__(self):
        self.ip_address = None
    def connect_wifi(self, ssid, password):
        if ssid == 'the ssid' and password == '12345678':
            self.ip_address = 'the ip address'
        return self.ip_address

class MockAccessPoint:
    def __init__(self):
        self.access_point_launched = False
    def launch(self):
        self.access_point_launched = True

class MockProgramOptionsReader:
    def read_program_options(self):
        return self.options

class TestNetworkInitialiser:
    def setup_method(self, test_method):
        self.mock_pico_wrapper = MockPicoWrapper()
        self.mock_progress = MockProgress()
        self.mock_wifi_connection = MockWiFiConnection()
        self.mock_access_point = MockAccessPoint()
        self.mock_program_options_reader = MockProgramOptionsReader()
 
        self.di = {}
        self.di['PicoWrapper'] = self.mock_pico_wrapper
        self.di['ProgramOptionsReader'] = self.mock_program_options_reader
        self.di['PicoAccessPoint'] = self.mock_access_point
        self.di['WiFiConnector'] = self.mock_wifi_connection
        self.di['ProgressIndicator'] = self.mock_progress
        self.initialiser = NetworkInitialiser(self.mock_progress, self.di)

    def test_if_the_options_file_is_not_found_the_access_point_is_launched(self):
        self.mock_program_options_reader.options = None

        self.initialiser.initialise()

        assert(self.mock_access_point.access_point_launched == True)
        assert(self.mock_pico_wrapper.logs == ['The options file was not found.'])

    def test_if_the_options_file_is_found_the_wifi_connection_is_initialised(self):
        self.mock_program_options_reader.options = {'ssid': 'the ssid', 'password': '12345678'}

        self.initialiser.initialise()

        assert(self.mock_wifi_connection.ip_address == 'the ip address')
        assert(self.mock_pico_wrapper.logs == ['Attempting to connect to the ssid-12345678','Connected as the ip address.'])

    def test_if_the_connection_succeeds_the_program_options_are_returned(self):
        self.mock_program_options_reader.options = {'ssid': 'the ssid', 'password': '12345678', 'option1': 'option 1' }

        options = self.initialiser.initialise()

        assert(options['ssid'] == 'the ssid')
        assert(options['password'] == '12345678')
        assert(options['option1'] == 'option 1')

    def test_if_the_connection_succeeds_the_program_options_include_the_ip_address(self):
        self.mock_program_options_reader.options = {'ssid': 'the ssid', 'password': '12345678', 'option1': 'option 1' }

        options = self.initialiser.initialise()

        assert(options['ip'] == 'the ip address')

    def test_if_the_connection_succeeds_the_timer_is_deinitialised(self):
        self.mock_program_options_reader.options = {'ssid': 'the ssid', 'password': '12345678', 'option1': 'option 1' }

        options = self.initialiser.initialise()

        assert(self.mock_progress.timer_has_been_deinitialised)

    def test_if_the_network_intialisation_fails_the_access_point_is_launched(self):
        self.mock_program_options_reader.options = {'ssid': 'the ssid', 'password': 'xxx', 'option1': 'option 1' }

        self.initialiser.initialise()

        assert(self.mock_access_point.access_point_launched == True)
        assert(self.mock_pico_wrapper.logs == ['Attempting to connect to the ssid-xxx','Connection failed.'])


    def test_if_the_reset_pin_is_set_low_the_credentials_file_is_deleted(self):
        self.mock_program_options_reader.options = {'ssid': 'the ssid', 'password': 'xxx', 'option1': 'option 1' }
        self.mock_pico_wrapper.reset_pin_value = False

        self.initialiser.initialise()

        assert(self.mock_access_point.access_point_launched == True)
        assert(self.mock_pico_wrapper.deleted_file == PROGRAM_OPTIONS_FILE)
