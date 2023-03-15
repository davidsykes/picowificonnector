class MockPicoWrapper:
    def __init__(self, credentials):
        self.credentials = credentials
        self.files = {}

    def read_file_data(self, path):
        return self.credentials

    def store_credentials(self, path, ssid, password):
        self.files[path] = ssid + "\n" + password

    def log(self, log):
        print('LOG:', log)

    def reset(self):
        print('RESET')