try:
 import usocket as socket
except:
 import socket
import network
import gc
from constants import PROGRAM_OPTIONS_FILE, MIN_HTTP
from progress_indicator import ProgressIndicator

HEAD_ACK = "<head><title>Parameters Accepted</title></head><body>"
DIV = '<div style="height:120px;font-size:70pt">'

class PicoAccessPoint:
    def __init__(self, di, access_point_options):
        self.ssid = access_point_options.ssid
        self.password = access_point_options.password
        self.options = access_point_options.options
        self.pico_wrapper = di['PicoWrapper']
        self.progress = di['ProgressIndicator']
        self.url_parameters_extractor = di['UrlParametersExtractor']
        self.access_point_form_creator = di['AccessPointFormCreator']

    def launch(self):
        self.progress.set_progress(ProgressIndicator.INITIALISING_ACCESS_POINT)
        gc.collect()
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=self.ssid, password=self.password)
        ap.active(True)

        while ap.active() == False:
            pass
        self.pico_wrapper.print('Connection is successful: %s' % str(ap.ifconfig()))
        self.progress.set_progress(ProgressIndicator.ACCESS_POINT_READY)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            self.pico_wrapper.print('Got a connection from %s' % str(addr))
            request = conn.recv(1024).decode()
            if request == 'reset':
               return
            parameters = self.url_parameters_extractor.extract_parameters(request)

            if 'ssid' in parameters:
                self.pico_wrapper.write_parameters_to_file(PROGRAM_OPTIONS_FILE, parameters)
                self.report_success(conn, parameters)
                conn.close()
                self.pico_wrapper.reset()
            else:
                response = self.access_point_form_creator.create_form(self.options)
                conn.send(response)
            conn.close()

    def report_success(self, conn, parameters):
        ssid = parameters['ssid']
        password = parameters['password']
        if 'show' in parameters:
            response = ''.join([MIN_HTTP, HEAD_ACK, DIV, 'OK<br>SSID: ', ssid, '<br>Password: ', password, '</div>'])
        else:
            response = ''.join([MIN_HTTP, HEAD_ACK, DIV, 'OK</div>'])
        conn.send(response)
