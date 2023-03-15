from constants import CREDENTIALS_FILE, LOG_FILE

class PicoWrapper:
    def read_file_data(self, path):
        try:
            file = open(path, 'r')
            content = file.read()
            print('File content', content)
            file.close()
            return content
        except OSError:
            return None
        
    def store_credentials(self, path, ssid, password):
        file = open(path, 'w')
        file.write(ssid + "\n" + password)
        file.close()
        
    def log(self, l, m=None):
        file = open(LOG_FILE, 'a')
        file.write(l + "\n")
        if m is not None:
            file.write(m + "\n")
        file.close()

    def reset(self):
        import machine
        machine.reset()
