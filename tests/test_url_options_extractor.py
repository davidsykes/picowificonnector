import sys
sys.path.append('../src')
from url_options_extractor import UrlOptionsExtractor

class MockPicoWrapper:
    def log(self, l):
        pass

class TestCredentialsExtractor:
    def setup_method(self, test_method):
        self.pico_wrapper = MockPicoWrapper()
        self.extractor = UrlOptionsExtractor(self.pico_wrapper)

    def test_a_simple_request_returns_no_password(self):
        request = 'GET / HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        (ssid,password,show) = self.extractor.extract_options(request)
        assert(ssid == None)
        assert(password == None)

    def test_a_simple_password_can_be_extracted(self):
        request = 'GET /?ssid=the_ssid&password=the_password&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        (ssid,password,show) = self.extractor.extract_options(request)
        assert(ssid == 'the_ssid')
        assert(password == 'the_password')

    def test_a_more_complicated_password_can_be_extracted(self):
        request = 'GET /?ssid=the_ssid&password=%3Fthisisthe&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        (ssid,password,show) = self.extractor.extract_options(request)
        assert(ssid == 'the_ssid')
        assert(password == '?thisisthe')
        
    def test_an_invalid_request_returns_no_password(self):
        request = '!'
        (ssid,password,show) = self.extractor.extract_options(request)
        assert(ssid == None)
        assert(password == None)
        
    def test_a_missing_request_returns_no_password(self):
        request = None
        (ssid,password,show) = self.extractor.extract_options(request)
        assert(ssid == None)
        assert(password == None)

    def test_show_is_false_when_the_shop_option_is_missing(self):
        request = 'GET /?ssid=the_ssid&password=the_password&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        (ssid,password,show) = self.extractor.extract_options(request)
        assert(show == False)

    def test_show_is_true_when_the_shop_option_is_present(self):
        request = 'GET /?ssid=the_ssid&password=the_password&show=y&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        (ssid,password,show) = self.extractor.extract_options(request)
        assert(show == True)
