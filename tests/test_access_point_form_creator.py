import sys
from machine import Pin, Timer
sys.path.append('../src')
from access_point_form_creator import AccessPointFormCreator

class TestAccessPointFormCreator:
    def setup_method(self, test_method):
        self.creator = AccessPointFormCreator()

    def test_the_basic_form_includes_ssid(self):
        form = self.creator.create_form(None)
        assert('input type="text" name="ssid"' in form)

    def test_the_basic_form_includes_password(self):
        form = self.creator.create_form(None)
        assert('input type="password" name="password"' in form)

    def test_the_basic_form_includes_show(self):
        form = self.creator.create_form(None)
        assert('input type="checkbox" id="show"' in form)