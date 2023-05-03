import re

class UrlParametersExtractor:
    def __init__(self, logger):
        self.logger = logger

    def extract_parameters(self, request):
        url_with_variables = self.take_first_line(request)
        variables_as_array = self.extract_variables(url_with_variables)
        variables_as_dictionary = self.create_dictionary(variables_as_array)
        return variables_as_dictionary

    def take_first_line(self, request):
        if request:
            return request.splitlines()[0]
        return ''

    def extract_variables(self, url_with_variables):
        match = re.match('GET /\\?([^ ]+)', url_with_variables)
        if match:
            groups = match.groups()
            if len(groups) == 1:
                variables = groups[0].split('&')
                return variables

    def create_dictionary(self, variables_as_array):
        parameters = {}
        if variables_as_array:
            for variable in variables_as_array:
                equals = variable.find('=')
                if equals > 0:
                    parameters[variable[0:equals]] = self.decode_percent(variable[equals+1:])
        return parameters

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
