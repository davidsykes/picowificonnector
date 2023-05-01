import sys
sys.path.append('../src')
from access_point_form_creator import AccessPointFormCreator
from access_point_option import AccessPointOption

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

    def test_the_basic_form_includes_show(self):
        form = self.creator.create_form(None)
        assert('input type="checkbox" id="show"' in form)

    def test_the_form_includes_added_options(self):
        form = self.creator.create_form([AccessPointOption('option1', 'option 1'),AccessPointOption('option2', 'option 2')])
        assert('input type="text" name="option1"' in form)
        assert('input type="text" name="option2"' in form)