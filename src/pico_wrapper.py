from constants import LOG_FILE

class PicoWrapper:
    def read_file_data(self, path):
        try:
            file = open(path, 'r')
            content = file.read()
            file.close()
            return content
        except OSError:
            return None
        
    def write_parameters_to_file(self, path, parameters):
        file = open(path, 'w')
        for key, value in parameters.items():
            file.write(''.join([key, '=', value, '\n']))
        file.close()

    def delete_file(self, path):
        import os
        os.remove(path)
        
    def log(self, l, m=None):
        s = l + "\n" + ('' if m is None else (m + "\n"))
        file = open(LOG_FILE, 'a')
        file.write(s)
        file.close()
        print(s)

    def reset(self):
        self.log('Reset')
        import machine
        machine.reset()

    def print(self, p):
        print(p)

    def create_input_pin_with_pullup(self, number):
        return Pin(number, Pin.IN, Pin.PULL_UP)