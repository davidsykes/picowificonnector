import sys
sys.path.append('../src')
from network_initialiser import NetworkInitialiser
from mock_pico_wrapper import MockPicoWrapper
import usocket
from constants import PROGRAM_OPTIONS_FILE
from access_point_option import AccessPointOption
from access_point_options import AccessPointOptions
from network import WLAN

class MockProgressIndicator:
    def __init__(self, pico):
        self.pico = pico
    def set_progress(self, progress, message=None):
        self.pico.print('PROGRESS ' + str(progress) + ('' if message is None else ('-'+message)))

def set_up_network_initialiser(verbose=False):
    pico = MockPicoWrapper(verbose)
    indicator = MockProgressIndicator(pico)
    di = { 'PicoWrapper': pico, 'ProgressIndicator' : indicator }
    connection = NetworkInitialiser(indicator, di)
    return connection,pico

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
    c,p = set_up_network_initialiser()
    usocket.socket.http_requests = [b'/',b'reset']

    access_point_options = AccessPointOptions('new ssid', 'new password')
    c.initialise(access_point_options)

    print('====', WLAN.access_point_ssid)
    assert(WLAN.access_point_ssid == 'new ssid')
    assert(WLAN.access_point_password == 'new password')

def when_displaying_the_access_point_when_an_extra_data_item_is_requested_it_is_stored_in_the_data_file():
    print('Display access point and request an extra parameter')
    c,p = set_up_network_initialiser()
    form_data = b'GET /?ssid=ssid&password=password&option1=option+1%2B2&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\n\r\n'
    usocket.socket.http_requests = [b'/', form_data, b'reset']

    access_point_options = AccessPointOptions('new ssid', 'new password', [AccessPointOption('option1', 'An option')])

    c.initialise(access_point_options)

    assert(p.files['options.txt'] == "ssid=ssid\npassword=password\noption1=option 1+2\nsubmit=Submit\n")

def when_credentials_have_been_supplied_a_connection_is_made():
    c,p = set_up_network_initialiser(True)
    p.options_file_data = "ssid=ssid\npassword=password"

    options = c.initialise(AccessPointOptions())

    assert(options['ip'] == 'ip address')

first_call_no_ssid_information_exists()
when_displaying_the_access_point_the_ssid_and_password_can_be_supplied()
when_displaying_the_access_point_the_ssid_and_password_can_be_modified()
when_displaying_the_access_point_when_an_extra_data_item_is_requested_it_is_stored_in_the_data_file()
when_credentials_have_been_supplied_a_connection_is_made()