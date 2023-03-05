class WLAN:
    status_values = [0]
    fail_on_connect = False
    def __init__(self, type):
        WLAN.type = type
    def active(self, state=None):
        if state is not None:
            WLAN.state = state
        return WLAN.state
    def connect(self, ssid, password):
        if self.fail_on_connect:
            raise Exception
    def status(self):
        if len(self.status_values) > 1:
            return self.status_values.pop(0)
        return self.status_values[0]
    def ifconfig(self):
        return ['ip address']
    def config(self, essid, password):
        WLAN.essid = essid
        WLAN.password = password

class STA_IF:
    pass
class AP_IF:
    pass