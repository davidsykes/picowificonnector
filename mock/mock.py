import sys
sys.path.append('../src')
from network_initialiser import NetworkInitialiser
from mock_pico_wrapper import MockPicoWrapper
import usocket
from constants import PROGRAM_OPTIONS_FILE

class MockProgressIndicator:
    def set_progress(self, message):
        pass

def set_up_network_initialiser():
    p = MockPicoWrapper(None)
    i = MockProgressIndicator()
    c = NetworkInitialiser('ssid', 'password', p, i)
    return c,p

def first_call_no_ssid_information_exists():
    print('No connection information exists')
    c,p = set_up_network_initialiser()
    usocket.socket.http_requests = [b'/',b'reset']

    c.initialise()

    assert(usocket.Connection.http_response[0:15] == "HTTP/1.0 200 OK")

def when_displaying_the_access_point_the_ssid_and_password_can_be_supplied():
    print('\nthe_access_point_is_created_and_the_parameters_supplied')
    c,p = set_up_network_initialiser()
    form_data = b'GET /?ssid=the_ssid&password=the_password&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
    usocket.socket.http_requests = [b'/', form_data, b'reset']

    c.initialise()

    assert(p.files[PROGRAM_OPTIONS_FILE] == "ssid=the_ssid\npassword=the_password\nsubmit=Submit\n")

def when_displaying_the_access_point_the_ssid_and_password_can_be_modified():
    print('Use different ssid and passwords')
    w = MockPicoWrapper(None)
    p = MockProgressIndicator()
    c = NetworkInitialiser(w, p)

    parameters = { 'ssid': 'new ssid', 'password': 'new password' }
    c.initialise(parameters)

    assert(False)

def when_displaying_the_access_point_when_an_extra_data_item_is_requested_it_is_stored_in_the_data_file():
    print('Display access point and request an extra parameter')
    w = MockPicoWrapper(None)
    p = MockProgressIndicator()
    c = NetworkInitialiser(w, p)
    form_data = b'GET /?ssid=the_ssid&password=the_password&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
    usocket.socket.http_requests = [b'/', form_data, b'reset']

    parameters = { 'options': [ { 'name': 'option1', 'text': 'An option'}] }

    c.initialise(parameters)

    assert(w.files['ssid.txt'] == "the_ssid\nthe_password\noption1=1234")

first_call_no_ssid_information_exists()
when_displaying_the_access_point_the_ssid_and_password_can_be_supplied()
when_displaying_the_access_point_the_ssid_and_password_can_be_modified()
when_displaying_the_access_point_when_an_extra_data_item_is_requested_it_is_stored_in_the_data_file()