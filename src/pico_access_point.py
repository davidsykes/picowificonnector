try:
 import usocket as socket        #importing socket
except:
 import socket
import network

SSID = 'PICO'
PASSWORD = '12345678'

class PicoAccessPoint:
    def __init__(self, progress):
        self.progress = progress
    def launch(self):
        self.progress.set_progress(7)
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=SSID, password=PASSWORD)
        ap.active(True)

        while ap.active() == False:
            pass
        self.progress.set_progress(8)

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating socket object
        s.bind(('', 80))
        s.listen(5)
        while True:
            conn, addr = s.accept()
            print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            print('Content = %s' % str(request))
            response = 'hello world'
            print('response=', response)
            conn.send(response)
            conn.close()