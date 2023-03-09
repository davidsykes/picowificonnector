class Connection:
    def __init__(self, http_request):
        self.http_request = http_request
    def recv(self, len):
        return self.http_request.encode()
    def send(self, data):
        Connection.http_response = data
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
        http_request = socket.http_requests.pop(0)
        return (Connection(http_request),'the mock network')

class AF_INET:
    pass
class SOCK_STREAM:
    pass