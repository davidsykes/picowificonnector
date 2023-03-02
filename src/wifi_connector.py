import network
import time

class WiFiConnector:
    def __init__(self, number_of_tries = 10, sleep_time = 1):
        pass
        self.number_of_tries = number_of_tries
#         self.sleep_time = sleep_time

    def connect_wifi(self, ssid, password):
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(ssid, password)

        number_of_tries = self.number_of_tries
        while number_of_tries > 0:
            if wlan.status() < 0 or wlan.status() >= 3:
                break
            number_of_tries -= 1
            time.sleep(1)

        # Check for connection
        if wlan.status() == 3:
#             status = wlan.ifconfig()
#             self.ip_address = status[0]
            return True
        return False