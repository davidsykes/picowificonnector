try:
 import usocket as socket
except:
 import socket
import network
import gc
from credentials_extractor import CredentialsExtractor
from constants import SSID, PASSWORD, CREDENTIALS_FILE

MIN_HTTP = 'HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n'

class PicoAccessPoint:
    def __init__(self, pico_wrapper, progress):
        self.pico_wrapper = pico_wrapper
        self.progress = progress
    def launch(self):
        self.progress.set_progress(7)
        gc.collect()
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=SSID, password=PASSWORD)
        ap.active(True)

        while ap.active() == False:
            pass
        print('Connection is successful:', ap.ifconfig())
        self.progress.set_progress(8)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 80))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024).decode()
            if request == 'reset':
               return
            (ssid,password) = CredentialsExtractor.extract_credentials(request, self.pico_wrapper)
            if ssid is not None:
               self.pico_wrapper.store_credentials(CREDENTIALS_FILE, ssid, password)
               conn.send(MIN_HTTP)
            else:
                response = MIN_HTTP + """<head>
    <title>SSID Input</title>
</head>
<body>
    <form>
        SSID:<br>
        <input type="text" name="ssid" style="height:60px;font-size:30pt" />
        <br>
        Password:<br>
        <input type="password" name="password" style="height:60px;font-size:30pt" />
        <br>
        <input type="submit" name="submit" value="Submit" />
    </form>
</body>
"""
                conn.send(response)
            conn.close()