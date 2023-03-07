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
            if request == 'reset':
               exit()
            else:
                response = """HTTP/1.0 200 OK
Content-type: text/html

<head>
    <title>SSID Input</title>
</head>
<body>
    <form >
        SSID : <input type = "text" name = "ssid" />
        <br>
        Password: <input type = "password" name = "password" />
        <input type = "submit" name = "submit" value = "Submit" />
    </form>
</body>
"""
                print('response=', response)
                conn.send(response)
            conn.close()