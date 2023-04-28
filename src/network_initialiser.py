from pico_wrapper import PicoWrapper
from wifi_connector import WiFiConnector
from pico_access_point import PicoAccessPoint
from url_parameters_extractor import UrlParametersExtractor
from program_options_reader import ProgramOptionsReader

class NetworkInitialiser:
    def __init__(self, progress_indicator = None, di = None):
        self.di = self._initialise_dependency_injection(di, progress_indicator)

    def _initialise_dependency_injection(self, di, progress_indicator):
        di = di or {}
        if 'PicoWrapper' not in di:
            di['PicoWrapper'] = PicoWrapper()
        if 'ProgramOptionsReader' not in di:
            di['ProgramOptionsReader'] = ProgramOptionsReader(di['PicoWrapper'])
        if 'UrlParametersExtractor' not in di:
            di['UrlParametersExtractor'] = UrlParametersExtractor(di['PicoWrapper'])
        if 'PicoAccessPoint' not in di:
            di['PicoAccessPoint'] = PicoAccessPoint('not right', 'wrong', di['PicoWrapper'], progress_indicator, di['UrlParametersExtractor'])
        return di

    def initialise(self, access_point_options = None):
        options = self.di['ProgramOptionsReader'].read_program_options()
        if options is not None:
            ssid = options['ssid']
            password = options['password']
            self.di['PicoWrapper'].log(''.join(['Attempting to connect to ', ssid, '-', password]))
            ip = self.di['WiFiConnector'].connect_wifi(ssid, password)
            if ip:
                self.di['PicoWrapper'].log(''.join(['Connected as ', ip, '.']))
                options['ip'] = ip
                return options
            else:
                self.di['PicoWrapper'].log('Connection failed.')
        else:
            self.di['PicoWrapper'].log('The options file was not found.')
        self.di['PicoAccessPoint'].launch()