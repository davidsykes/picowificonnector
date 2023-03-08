import sys
sys.path.append('../src')
from network_initialiser import NetworkInitialiser
from mock_pico_wrapper import MockPicoWrapper
import usocket

class MockProgressIndicator:
    def set_progress(self, value):
        pass

def first_call_no_ssid_information_exists():
    print('No connection information exists')

    w = MockPicoWrapper(None)
    p = MockProgressIndicator()
    c = NetworkInitialiser(w, p)
    usocket.socket.http_requests = ['/','reset']

    c.initialise()

    assert(usocket.Connection.http_response[0:15] == "HTTP/1.0 200 OK")

def the_access_point_is_created_and_the_credentials_supplied():
    print('the_access_point_is_created_and_the_credentials_supplied')
    w = MockPicoWrapper(None)
    p = MockProgressIndicator()
    c = NetworkInitialiser(w, p)
    form_data = 'GET /?ssid=the_ssid&password=the_password&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
    usocket.socket.http_requests = ['/', form_data, 'reset']

    c.initialise()

    assert(w.files['ssid.txt'] == "the_ssid\nthe_password")



first_call_no_ssid_information_exists()
the_access_point_is_created_and_the_credentials_supplied()