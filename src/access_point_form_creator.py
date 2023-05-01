from constants import MIN_HTTP

HEAD_INPUT = "<head><title>SSID Input</title></head><body>"

class AccessPointFormCreator:
    def create_form(self, options=None):
        form = MIN_HTTP + HEAD_INPUT + """
    <form style="height:120px;font-size:70pt">
        SSID:<br>
        <input type="text" name="ssid" style="height:120px;font-size:70pt"/>
        <br>
        Password:<br>
        <input type="password" name="password" style="height:120px;font-size:70pt"/>
        <br />
        <input type="checkbox" id="show" name="show" value="y" style="height:120px;width:120px"/>
        Report details?
        <br>
        <br>
        <input type="submit" name="submit" value="Submit" style="height:120px;font-size:70pt"/>
    </form>
</body>
"""
        return form