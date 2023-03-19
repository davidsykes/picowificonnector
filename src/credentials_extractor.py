import re

class CredentialsExtractor:
    def __init__(self, logger):
        self.logger = logger

    def extract_credentials(self, request):
        if request:
            line = request.splitlines()[0]
            self.logger.log(''.join(['Credentials: "', line, '"']))
            m = re.match(r"GET /\?ssid=([^ &]+)&password=([^ &]+)(&show=)?", line)
            if m and len(m.groups()) >= 2:
                ssid = self.decode_percent(m.group(1))
                password = self.decode_percent(m.group(2))
                show = m.group(3) is not None
                return(ssid, password,show)
        return(None,None,False)
    
    def decode_percent(self, sdata):
        pieces = sdata.split('%')
        sections = [pieces[0]]
        for Item in pieces[1:]:
            code = Item[:2]
            char = chr(int(code, 16))
            sections.append(char)
            sections.append(Item[2:].replace('+', ' '))
        Res = ''.join(sections)
        return Res
