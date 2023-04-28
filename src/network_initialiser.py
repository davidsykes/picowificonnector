from pico_wrapper import PicoWrapper
from progress_indicator import ProgressIndicator
from wifi_connector import WiFiConnector
from pico_access_point import PicoAccessPoint
from url_parameters_extractor import UrlParametersExtractor
from program_options_reader import ProgramOptionsReader

class NetworkInitialiser:
    def __init__(self, access_point_options=None, pico_wrapper=None, progress=None, wifi_connector=None, access_point = None, parameters_extractor = None, program_options_reader = None):
        self.access_point_options = access_point_options
        self.pico_wrapper = pico_wrapper or PicoWrapper()
        self.progress = progress or ProgressIndicator()
        self.wifi_connector = wifi_connector or WiFiConnector(self.progress)
        self.access_point = access_point
        self.parameters_extractor = parameters_extractor or UrlParametersExtractor(self.pico_wrapper)
        self.program_options_reader = program_options_reader or ProgramOptionsReader(self.pico_wrapper)

    def initialise(self):
        options = self.program_options_reader.read_program_options()
        if options is not None:
            ssid = options['ssid']
            password = options['password']
            self.pico_wrapper.log(''.join(['Attempting to connect to ', ssid, '-', password]))
            ip = self.wifi_connector.connect_wifi(ssid, password)
            if ip:
                self.pico_wrapper.log(''.join(['Connected as ', ip, '.']))
                options['ip'] = ip
                return options
            else:
                self.pico_wrapper.log('Connection failed.')
        else:
            self.pico_wrapper.log('The options file was not found.')
        access_point = self.access_point or PicoAccessPoint(self.ssid, self.password, self.pico_wrapper, self.progress, self.parameters_extractor)
        access_point.launch()