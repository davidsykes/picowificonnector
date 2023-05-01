import sys
sys.path.append('../src')
from url_parameters_extractor import UrlParametersExtractor

class MockPicoWrapper:
    def log(self, l):
        pass

class TestUrlParametersExtractor:
    def setup_method(self, test_method):
        self.pico_wrapper = MockPicoWrapper()
        self.extractor = UrlParametersExtractor(self.pico_wrapper)

    def test_a_simple_request_returns_no_password(self):
        request = 'GET / HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        parameters = self.extractor.extract_parameters(request)
        assert('ssid' not in parameters)
        assert('password' not in parameters)

    def test_a_simple_password_can_be_extracted(self):
        request = 'GET /?ssid=the_ssid&password=the_password&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\nConnection: keep-alive\r\nUpgrade-Insecure-Requests: 1\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8\r\nUser-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 16_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Mobile/15E148 Safari/604.1\r\nReferer: http://192.168.4.1/\r\nAccept-Language: en-GB,en;q=0.9\r\nAccept-Encoding: gzip, deflate\r\n\r\n'
        parameters = self.extractor.extract_parameters(request)
        assert('ssid' in parameters)
        assert('password' in parameters)
        assert(parameters['ssid'] == 'the_ssid')
        assert(parameters['password'] == 'the_password')

    def test_a_more_complicated_password_can_be_extracted(self):
        request = 'GET /?ssid=the_ssid&password=%3Fthisisthe&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\n'
        parameters = self.extractor.extract_parameters(request)
        assert(parameters['ssid'] == 'the_ssid')
        assert(parameters['password'] == '?thisisthe')
        
    def test_an_invalid_request_returns_no_password(self):
        request = '!'
        parameters = self.extractor.extract_parameters(request)
        assert('ssid' not in parameters)
        assert('password' not in parameters)
        
    def test_a_missing_request_returns_no_password(self):
        request = None
        parameters = self.extractor.extract_parameters(request)
        assert('ssid' not in parameters)
        assert('password' not in parameters)

    def test_the_show_is_options_is_returned(self):
        request = 'GET /?ssid=the_ssid&password=the_password&show=yo&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\n'
        parameters = self.extractor.extract_parameters(request)
        assert(parameters['show'] == 'yo')

    def test_additional_options_are_returned(self):
        request = 'GET /?ssid=the_ssid&password=the_password&show=yo&option1=option%201&show=yo&option2=option%202&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\n'
        parameters = self.extractor.extract_parameters(request)
        assert(parameters['option1'] == 'option 1')
        assert(parameters['option2'] == 'option 2')

    def test_spaces_can_be_represented_by_plus_signs(self):
        request = 'GET /?ssid=the_ssid&password=the_password&show=yo&option1=option+1&show=yo&option2=option+2&submit=Submit HTTP/1.1\r\nHost: 192.168.4.1\r\n'
        parameters = self.extractor.extract_parameters(request)
        assert(parameters['option1'] == 'option 1')
        assert(parameters['option2'] == 'option 2')
