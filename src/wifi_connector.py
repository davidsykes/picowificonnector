import network
import time

class WiFiConnector:
    def __init__(self, progress,  number_of_tries = 10, sleep_time = 1):
        self.number_of_tries = number_of_tries
        self.sleep_time = sleep_time
        self.progress = progress

    def connect_wifi(self, ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)
        self.progress.set_progress(3)

        number_of_tries = self.number_of_tries
        while number_of_tries > 0:
            status = wlan.status()
            if status < 0:
                self.progress.set_progress(4)
                return False
            if status == 3:
                self.progress.set_progress(5)
                return True
            number_of_tries -= 1
            time.sleep(self.sleep_time)
        self.progress.set_progress(6)
        return False
