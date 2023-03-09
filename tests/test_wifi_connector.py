import sys
import network
sys.path.append('../src')
from wifi_connector import WiFiConnector
from progress_indicator import ProgressIndicator

class MockProgress:
    def __init__(self):
        self.value = 0
    def set_progress(self, value):
        self.value = value

class TestWiFiConnector:
    def setup_method(self, test_method):
        network.WLAN.fail_on_connect = False
        self.mock_progress = MockProgress()
        self.connector = WiFiConnector(self.mock_progress, 3, 0.001)

    def test_connection_type_sta_if_is_made(self):
        self.connector.connect_wifi('ssid','12345678')

        assert(network.WLAN.type == network.STA_IF)

    def test_when_a_connection_can_not_be_made_false_is_returned(self):
        network.WLAN.status_values = [0,1,2,3]

        ret = self.connector.connect_wifi('ssid','12345678')

        assert(ret == False)

    def test_the_connector_tries_several_times(self):
        network.WLAN.status_values = [1,2,3]

        ret = self.connector.connect_wifi('ssid','12345678')

        assert(ret == True)

    def test_if_status_is_negative_the_connection_fails(self):
        network.WLAN.status_values = [-1,3]

        ret = self.connector.connect_wifi('ssid','12345678')

        assert(ret == False)

    def test_if_status_becomes_3_the_connection_succeeds(self):
        network.WLAN.status_values = [1,3]

        ret = self.connector.connect_wifi('ssid','12345678')

        assert(ret == True)

    def test_if_status_does_not_connect_the_connection_fails(self):
        network.WLAN.status_values = [1,1,1,1,1,1,1,1,1,1,1,1,1]

        ret = self.connector.connect_wifi('ssid','12345678')

        assert(ret == False)

    def test_if_connect_succeeds_progress_is_set(self):
        network.WLAN.status_values = [3]

        self.connector.connect_wifi('ssid','12345678')

        assert(self.mock_progress.value == ProgressIndicator.CONNECTED)

    def test_if_wlan_connect_fails_the_progress_is_not_updated(self):
        network.WLAN.fail_on_connect = True

        try:
            self.connector.connect_wifi('ssid','12345678')
        except:
            pass

        assert(self.mock_progress.value == ProgressIndicator.CONNECTING)

    def test_if_connection_fails_progress_is_set(self):
        network.WLAN.status_values = [-1]

        self.connector.connect_wifi('ssid','12345678')

        assert(self.mock_progress.value == ProgressIndicator.NETWORK_ERROR)

    def test_if_connection_fails_progress_is_set(self):
        network.WLAN.status_values = [0]

        self.connector.connect_wifi('ssid','12345678')

        assert(self.mock_progress.value == ProgressIndicator.CONNECTING_TIMED_OUT)