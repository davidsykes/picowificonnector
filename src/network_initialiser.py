from pico_wrapper import PicoWrapper
from progress_indicator import ProgressIndicator
from wifi_connector import WiFiConnector
from pico_access_point import PicoAccessPoint
from constants import CREDENTIALS_FILE
from credentials_extractor import CredentialsExtractor

class NetworkInitialiser:
    def __init__(self, ssid = 'PICO', password = '12345678', pico_wrapper=None, progress=None, wifi_connector=None, access_point = None, credentials_extractor = None):
        self.ssid = ssid
        self.password = password
        self.pico_wrapper = pico_wrapper or PicoWrapper()
        self.progress = progress or ProgressIndicator()
        self.wifi_connector = wifi_connector or WiFiConnector(self.progress)
        self.access_point = access_point
        self.credentials_extractor = credentials_extractor or CredentialsExtractor(self.pico_wrapper)

    def initialise(self):
        credentials = self.read_credentials()
        if credentials is not None:
            self.pico_wrapper.log(''.join(['Attempting to connect to ',credentials[0], '-', credentials[1]]))
            enabled = self.wifi_connector.connect_wifi(credentials[0], credentials[1])
            if enabled:
                self.pico_wrapper.log('Connected.')
                return
            else:
                self.pico_wrapper.log('Connection failed.')
        else:
            self.pico_wrapper.log('The credentials file was not found.')
        access_point = self.access_point or PicoAccessPoint(self.ssid, self.password, self.pico_wrapper, self.progress, self.credentials_extractor)
        access_point.launch()

    def read_credentials(self):
        self.progress.set_progress(ProgressIndicator.READ_CREDENTIALS)
        credential_text = self.pico_wrapper.read_file_data(CREDENTIALS_FILE)
        if credential_text is not None:
            return credential_text.splitlines()[0:2]