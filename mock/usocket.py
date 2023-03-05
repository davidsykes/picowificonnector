class Connection:
    def recv(self, len):
        return ''
    def send(self, data):
        pass
    def close(self):
        pass

class socket:
    def __init__(self, type1, type2):
        pass
    def bind(self, a):
        pass
    def listen(self, n):
        pass
    def accept(self):
        return (Connection(),'')

class AF_INET:
    pass
class SOCK_STREAM:
    pass