from constants import RESET_PIN, PROGRAM_OPTIONS_FILE

class MockPin:
    reset_pin_value = 1
    def __init__(self, number):
        if number == RESET_PIN:
            self._value = MockPin.reset_pin_value
        else:
            self._value = 1
    def value(self):
        return self._value

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

    def create_input_pin_with_pullup(self, number):
        return MockPin(number)
    
    def delete_file(self, path):
        if path == PROGRAM_OPTIONS_FILE:
            self.options_file_data = None