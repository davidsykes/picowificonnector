try:
 import usocket as socket
except:
 import socket
import network
import gc
from constants import PROGRAM_OPTIONS_FILE
from progress_indicator import ProgressIndicator

MIN_HTTP = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'
HEAD_INPUT = "<head><title>SSID Input</title></head><body>"
HEAD_ACK = "<head><title>Parameters Accepted</title></head><body>"
DIV = '<div style="height:120px;font-size:70pt">'

class PicoAccessPoint:
    def __init__(self, ssid, password, pico_wrapper, progress, parameters_extractor):
        self.ssid = ssid
        self.password = password
        self.pico_wrapper = pico_wrapper
        self.progress = progress
        self.parameters_extractor = parameters_extractor

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
            parameters = self.parameters_extractor.extract_parameters(request)

            if 'ssid' in parameters:
                self.pico_wrapper.store_parameters(PROGRAM_OPTIONS_FILE, parameters)
                self.report_success(conn, parameters)
                conn.close()
                self.pico_wrapper.reset()
            else:
                response = MIN_HTTP + HEAD_INPUT + """
    <form style="height:120px;font-size:70pt">
        SSID:<br>
        <input type="text" name="ssid" style="height:120px;font-size:70pt"/>
        <br>
        Password:<br>
        <input type="password" name="password" style="height:120px;font-size:70pt"/>
        <br />
        <input type="checkbox" id="show" name="show" value="y" style="height:120px;width:120px"/>
        Report details?
        <br>
        <br>
        <input type="submit" name="submit" value="Submit" style="height:120px;font-size:70pt"/>
    </form>
</body>
"""
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
