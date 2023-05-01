class MockPicoWrapper:
    def __init__(self, verbose):
        self.verbose = verbose
        self.files = {}
        self.options_file_data = None

    def read_file_data(self, path):
        return self.options_file_data

    def write_parameters_to_file(self, path, parameters):
        params = ''
        for key, value in parameters.items():
            params = params + ''.join([key, '=', value, '\n'])
        self.files[path] = params

    def log(self, log):
        if self.verbose:
            print('    log:', log)

    def reset(self):
        if self.verbose:
            print('RESET')

    def print(self, p):
        if self.verbose:
            print('   ', p)