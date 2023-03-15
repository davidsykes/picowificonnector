import re

class CredentialsExtractor:
    def extract_credentials(request, logger):
        if request:
            line = request.splitlines()[0]
            logger.log(''.join(['Credentials: "', line, '"']))
            m = re.match(r"GET /\?ssid=([^ &]+)&password=([^ &]+)", line)
            if m and len(m.groups()) == 2:
                ssid = CredentialsExtractor.decode_percent(m.group(1))
                password = CredentialsExtractor.decode_percent(m.group(2))
                return(ssid, password)
        return(None,None)
    
    def decode_percent(sdata):
        pieces = sdata.split('%')
        sections = [pieces[0]]
        for Item in pieces[1:]:
            code = Item[:2]
            char = chr(int(code, 16))
            sections.append(char)
            sections.append(Item[2:].replace('+', ' '))
        Res = ''.join(sections)
        return Res
