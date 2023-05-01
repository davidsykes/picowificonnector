from constants import MIN_HTTP

HEAD_INPUT = '<head><title>SSID Input</title></head><body>'
FORM_STYLE = '<form style="height:120px;font-size:70pt">'
STYLE = 'style="height:120px;font-size:70pt"'

class AccessPointFormCreator:
    def create_form(self, options=None):
        form = MIN_HTTP + HEAD_INPUT + FORM_STYLE
        form += self._make_input('SSID', 'text', 'ssid')
        form += self._make_input('Password', 'password', 'password')

        if (options):
            for option in options:
                form += self._make_input(option.text, 'text', option.name)

        form += '<input type="checkbox" id="show" name="show" value="y" style="height:120px;width:120px"/>Report details?<br>'
        form += ''.join(['<br><input type="submit" name="submit" value="Submit" ', STYLE, '/>'])
        form += '</form></body>'
        return form
    
    def _make_input(self, text, type, name):
        return ''.join([text, ':<br><input type="', type, '" name="', name, '" ', STYLE, '/><br>'])