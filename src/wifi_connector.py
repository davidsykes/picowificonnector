import network
import time

class WiFiConnector:
    def __init__(self, progress,  number_of_tries = 10, sleep_time = 1):
        self.number_of_tries = number_of_tries
        self.sleep_time = sleep_time
        self.progress = progress

    def connect_wifi(self, ssid, password):
        self.progress.set_progress(1)
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        self.progress.set_progress(2)

        number_of_tries = self.number_of_tries
        while number_of_tries > 0:
            status = wlan.status()
            if status < 0 or status >= 3:
                break
            number_of_tries -= 1
            time.sleep(self.sleep_time)

        # Check for connection
        if wlan.status() == 3:
#             status = wlan.ifconfig()
#             self.ip_address = status[0]
            self.progress.set_progress(3)
            return True
        return False