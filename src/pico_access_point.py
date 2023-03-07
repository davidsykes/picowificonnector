try:
 import usocket as socket
except:
 import socket
import network
import gc

SSID = 'PICO'
PASSWORD = '12345678'

class PicoAccessPoint:
    def __init__(self, progress):
        self.progress = progress
    def launch(self):
        self.progress.set_progress(7)
        gc.collect()
        ap = network.WLAN(network.AP_IF)
        ap.config(essid=SSID, password=PASSWORD)
        ap.active(True)

        while ap.active() == False:
            pass
        print('Connection is successful')
        print(ap.ifconfig())



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
        SSID : <input type = "text" name = "ssid" style="height:500pxfont-size:14pt/>
        <br>
        Password: <input type = "password" name = "password" style="height:500pxfont-size:14pt/>
        <input type = "submit" name = "submit" value = "Submit" />
    </form>
</body>
"""
                conn.send(response)
            conn.close()