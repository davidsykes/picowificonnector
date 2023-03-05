import sys
sys.path.append('../src')
from network_initialiser import NetworkInitialiser
from mock_pico_wrapper import MockPicoWrapper
from mock_progress_indicator import MockProgressIndicator

def first_call_no_ssid_information_exists():
    print('No connection information exists')

    w = MockPicoWrapper(None)
    p = MockProgressIndicator()
    c = NetworkInitialiser(w, p)
    c.initialise()

    assert(p.progress == 5)

first_call_no_ssid_information_exists()