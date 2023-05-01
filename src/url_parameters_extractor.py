import re

class UrlParametersExtractor:
    def __init__(self, logger):
        self.logger = logger

    def extract_parameters(self, request):
        parameters = {}
        if request:
            line = self.split_and_remove_prefix(request)
            match = re.findall(r"([^& ]+)", line )
            for param in match:
                equals = param.find('=')
                if equals > 0:
                    parameters[param[0:equals]] = self.decode_percent(param[equals+1:])
        return parameters
    
    def split_and_remove_prefix(self, request):
        line = request.splitlines()[0]
        pos = line.find('?')
        return line[pos+1:]

    def decode_percent(self, sdata):
        pieces = sdata.split('%')
        sections = [pieces[0].replace('+', ' ')]
        for Item in pieces[1:]:
            code = Item[:2]
            char = chr(int(code, 16))
            sections.append(char)
            sections.append(Item[2:].replace('+', ' '))
        Res = ''.join(sections)
        return Res
