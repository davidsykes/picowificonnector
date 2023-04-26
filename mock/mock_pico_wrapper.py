class MockPicoWrapper:
    def __init__(self, parameters):
        self.parameters = parameters
        self.files = {}

    def read_file_data(self, path):
        return self.parameters

    def store_parameters(self, path, ssid, password):
        self.files[path] = ssid + "\n" + password

    def log(self, log):
        print('LOG:', log)

    def reset(self):
        print('RESET')

    def print(self, p):
        print(p)