import sys
sys.path.append('../src')
from program_options_reader import ProgramOptionsReader

class MockPicoWrapper:
    def read_file_data(self, path):
        return self.file_data

class TestProgramOptions:
    def setup_method(self, test_method):
        self.mock_pico_wrapper = MockPicoWrapper()
        self.options = ProgramOptionsReader(self.mock_pico_wrapper)

    def test_if_the_file_does_not_exist_None_is_returned(self):
        self.mock_pico_wrapper.file_data = None

        options = self.options.read_program_options()

        assert(options is None)
        
    def test_if_the_file_exists_options_are_defined_by_an_equal_sign(self):
        self.mock_pico_wrapper.file_data = "SSID=ssid\npassword=18273645\noption=option 1"

        options = self.options.read_program_options()

        assert(options['SSID'] == 'ssid')
        assert(options['password'] == '18273645')
        assert(options['option'] == 'option 1')

    def test_options_are_split_by_the_first_equals_sign(self):
        self.mock_pico_wrapper.file_data = "SSID=ssid\npassword=18273645\noption=option==1"

        options = self.options.read_program_options()

        assert(options['SSID'] == 'ssid')
        assert(options['password'] == '18273645')
        assert(options['option'] == 'option==1')

