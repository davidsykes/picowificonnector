class MockPicoWrapper:
    def __init__(self, parameters):
        self.parameters = parameters
        self.files = {}

    def read_file_data(self, path):
        return self.parameters

    def write_parameters_to_file(self, path, parameters):
        params = ''
        for key, value in parameters.items():
            params = params + ''.join([key, '=', value, '\n'])
        self.files[path] = params

    def log(self, log):
        print('    log:', log)

    def reset(self):
        print('RESET')

    def print(self, p):
        print('   ', p)