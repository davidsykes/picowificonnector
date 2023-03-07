import sys
sys.path.append('../src')
from network_initialiser import NetworkInitialiser
from mock_pico_wrapper import MockPicoWrapper
from mock_progress_indicator import MockProgressIndicator
import usocket

def first_call_no_ssid_information_exists():
    print('No connection information exists')

    w = MockPicoWrapper(None)
    p = MockProgressIndicator()
    c = NetworkInitialiser(w, p)
    usocket.socket.http_requests = ['/','reset']

    c.initialise()

    assert(w.web_page[0:15] == "HTTP/1.0 200 OK")

first_call_no_ssid_information_exists()