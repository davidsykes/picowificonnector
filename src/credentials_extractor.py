import re

class CredentialsExtractor:
    def extract_credentials(request, logger):
        if request:
            line = request.splitlines()[0]
            logger.log(''.join(['Credentials: "', line, '"']))
            m = re.match(r"GET /\?ssid=([^ &]+)&password=([^ &]+)", line)
            if m and len(m.groups()) == 2:
                ssid = m.group(1)
                password = m.group(2)
                return(ssid, password)
        return(None,None)