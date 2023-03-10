import sys
sys.path.append('../src')
from credentials_extractor import CredentialsExtractor

class MockPicoWrapper:
    def log(self, l):
        pass

class TestCredentialsExtractor:
    def setup_method(self, test_method):
        self.pico_wrapper = MockPicoWrapper()

    def test_a_simple_request_returns_no_password(self):
        request = 'GET / HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        (ssid,password) = CredentialsExtractor.extract_credentials(request, self.pico_wrapper)
        assert(ssid == None)
        assert(password == None)

    def test_a_simple_password_can_be_extracted(self):
        request = 'GET /?ssid=the_ssid&password=the_password&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        (ssid,password) = CredentialsExtractor.extract_credentials(request, self.pico_wrapper)
        assert(ssid == 'the_ssid')
        assert(password == 'the_password')
        
    def test_an_invalid_request_returns_no_password(self):
        (ssid,password) = CredentialsExtractor.extract_credentials('!', self.pico_wrapper)
        assert(ssid == None)
        assert(password == None)
        
    def test_a_missing_request_returns_no_password(self):
        (ssid,password) = CredentialsExtractor.extract_credentials(None, self.pico_wrapper)
        assert(ssid == None)
        assert(password == None)
