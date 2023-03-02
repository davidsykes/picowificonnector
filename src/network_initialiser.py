from wifi_connector import WiFiConnector

class NetworkInitialiser:
    def __init__(self, pico_wrapper, wifi_connector=None, hotspot = None):
        self.pico_wrapper = pico_wrapper
        self.wifi_connector = wifi_connector or WiFiConnector()
        self.hotspot = hotspot

    def initialise(self):
        credentials = self.read_credentials()
        if credentials is not None:
            enabled = self.wifi_connector.connect_wifi(credentials[0], credentials[1])
            if enabled:
                return
        hotspot = self.hotspot or PicoHotspot()
        hotspot.launch()

    def read_credentials(self):
        credential_text = self.pico_wrapper.read_file_data('ssid.txt')
        if credential_text is not None:
            return credential_text.splitlines()[0:2]