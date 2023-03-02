class WLAN:
    status_values = [0]
    def __init__(self, sta_if):
        pass
    def active(self, state):
        pass
    def connect(self, ssid, password):
        pass
    def status(self):
        if len(self.status_values) > 1:
            return self.status_values.pop(0)
        return self.status_values[0]
    def ifconfig(self):
        return ['ip address']

class STA_IF:
    pass