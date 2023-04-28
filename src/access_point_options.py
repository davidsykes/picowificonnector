class AccessPointOptions:
    def __init__(self, ssid=None, password=None, options=None):
        self.ssid = ssid or 'PICO'
        self.password = password or '12345678'
        self.options = options or []