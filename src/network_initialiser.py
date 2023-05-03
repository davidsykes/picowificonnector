from pico_wrapper import PicoWrapper
from pico_access_point import PicoAccessPoint
from program_options_reader import ProgramOptionsReader
from access_point_options import AccessPointOptions
from progress_indicator import ProgressIndicator
from url_parameters_extractor import UrlParametersExtractor
from access_point_form_creator import AccessPointFormCreator
from wifi_connector import WiFiConnector

class NetworkInitialiser:
    def __init__(self, progress_indicator = None, di = None):
        self.di = self._initialise_dependency_injection(di, progress_indicator)
        self.program_options_reader = self.di['ProgramOptionsReader']
        self.pico_wrapper = self.di['PicoWrapper']
        self.progress_indicator = self.di['ProgressIndicator']

    def _initialise_dependency_injection(self, di, progress_indicator):
        di = di or {}
        if 'PicoWrapper' not in di:
            di['PicoWrapper'] = PicoWrapper()
        if 'ProgramOptionsReader' not in di:
            di['ProgramOptionsReader'] = ProgramOptionsReader(di['PicoWrapper'])
        if 'ProgressIndicator' not in di:
            di['ProgressIndicator'] = progress_indicator or ProgressIndicator()
        if 'UrlParametersExtractor' not in di:
            di['UrlParametersExtractor'] = UrlParametersExtractor(di['PicoWrapper'])
        if 'AccessPointFormCreator' not in di:
            di['AccessPointFormCreator'] = AccessPointFormCreator()
        if 'WiFiConnector' not in di:
            di['WiFiConnector'] = WiFiConnector(di['ProgressIndicator'])
        return di

    def initialise(self, access_point_options = None):
        self.progress_indicator.set_progress(ProgressIndicator.LOOKING_FOR_EXISTING_DETAILS)
        options = self.program_options_reader.read_program_options()
        if options is not None:
            ssid = options['ssid']
            password = options['password']
            self.pico_wrapper.log(''.join(['Attempting to connect to ', ssid, '-', password]))
            ip = self.di['WiFiConnector'].connect_wifi(ssid, password)
            if ip:
                self.pico_wrapper.log(''.join(['Connected as ', ip, '.']))
                options['ip'] = ip
                return options
            else:
                self.pico_wrapper.log('Connection failed.')
        else:
            self.pico_wrapper.log('The options file was not found.')
        self._launch_access_point(access_point_options)

    def _launch_access_point(self, access_point_options):
        if 'PicoAccessPoint' in self.di:
            launcher = self.di['PicoAccessPoint']
        else:
            launcher = PicoAccessPoint(self.di, access_point_options or AccessPointOptions())
        launcher.launch()