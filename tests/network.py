class WLAN:
    status_values = [0]
    fail_on_connect = False
    def __init__(self, sta_if):
        pass
    def active(self, state):
        pass
    def connect(self, ssid, password):
        if self.fail_on_connect:
            raise Exception
    def status(self):
        if len(self.status_values) > 1:
            return self.status_values.pop(0)
        return self.status_values[0]
    def ifconfig(self):
        return ['ip address']

class STA_IF:
    pass