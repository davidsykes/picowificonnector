import sys
import network
sys.path.append('../src')
from wifi_connector import WiFiConnector

class TestWiFiConnector:
    def setup_method(self, test_method):
        self.connector = WiFiConnector(3, 0.001)

    def test_when_a_connection_can_not_be_made_false_is_returned(self):
        network.WLAN.status_values = [0,1,2,3]

        ret = self.connector.connect_wifi('ssid','12345678')

        assert(ret == False)

    def test_the_connector_tries_several_times(self):
        network.WLAN.status_values = [0,1,3]

        ret = self.connector.connect_wifi('ssid','12345678')

        assert(ret == True)
