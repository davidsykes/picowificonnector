class MockPicoWrapper:
    def __init__(self, credentials):
        self.credentials = credentials

    def read_file_data(self, path):
        return self.credentials