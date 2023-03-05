from pico_wrapper import PicoWrapper
from progress_indicator import ProgressIndicator
from wifi_connector import WiFiConnector
from pico_access_point import PicoAccessPoint

class NetworkInitialiser:
    def __init__(self, pico_wrapper=None, progress=None, wifi_connector=None, access_point = None):
        self.pico_wrapper = pico_wrapper or PicoWrapper()
        self.progress = progress or ProgressIndicator()
        self.wifi_connector = wifi_connector or WiFiConnector(self.progress)
        self.access_point = access_point

    def initialise(self):
        self.progress.set_progress(1)
        credentials = self.read_credentials()
        if credentials is not None:
            self.progress.set_progress(2)
            enabled = self.wifi_connector.connect_wifi(credentials[0], credentials[1])
            if enabled:
                return
        access_point = self.access_point or PicoAccessPoint(self.progress)
        access_point.launch()

    def read_credentials(self):
        credential_text = self.pico_wrapper.read_file_data('ssid.txt')
        if credential_text is not None:
            return credential_text.splitlines()[0:2]