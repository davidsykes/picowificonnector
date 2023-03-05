class PicoWrapper:
    def read_file_data(self, path):
        try:
            file = open(path, 'r')
            content = file.read()
            print('content', content)
            file.close()
            return conent
        except OSError:
            return None