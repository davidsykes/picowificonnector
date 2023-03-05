import sys
import network
sys.path.append('../src')
from pico_access_point import PicoAccessPoint

class MockProgress:
    def __init__(self):
        self.value = 0
    def set_progress(self, value):
        self.value = value

class TestPicoAccessPoint:
    def setup_method(self, test_method):
        self.mock_progress = MockProgress()
        self.ap = PicoAccessPoint(self.mock_progress)

    def test_an_access_point_is_initialised(self):
        self.ap.launch()

        assert(network.WLAN.type == network.AP_IF)
        assert(network.WLAN.essid == 'PICO')
        assert(network.WLAN.password == '12345678')