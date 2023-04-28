import sys
sys.path.append('../src')
from access_point_options import AccessPointOptions
from access_point_option import AccessPointOption

class TestAccessPointOptions:
    def test_if_no_options_are_supplied_defaults_are_used(self):
        options = AccessPointOptions(None)

        assert(options.ssid == 'PICO')
        assert(options.password == '12345678')
        assert(options.options == [])

    def test_ssid_and_password_can_be_supplied(self):
        options = AccessPointOptions('the ssid', 'the password')

        assert(options.ssid == 'the ssid')
        assert(options.password == 'the password')

    def test_if_no_ssid_is_supplied_defaults_are_used(self):
        options = AccessPointOptions(password = 'the password')

        assert(options.ssid == 'PICO')
        assert(options.password == 'the password')

    def test_if_no_password_is_supplied_defaults_are_used(self):
        options = AccessPointOptions(ssid = 'the ssid')

        assert(options.ssid == 'the ssid')
        assert(options.password == '12345678')

    def test_options_can_be_supplied(self):
        options = AccessPointOptions(options = [ AccessPointOption('name', 'text')])

        assert(len(options.options) == 1)
        assert(options.options[0].name == 'name')
        assert(options.options[0].text == 'text')