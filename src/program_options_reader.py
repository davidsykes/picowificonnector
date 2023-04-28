from constants import PROGRAM_OPTIONS_FILE

class ProgramOptionsReader:
    def __init__(self, pico_wrapper) -> None:
        self.pico_wrapper = pico_wrapper

    def read_program_options(self):
        options_text = self.pico_wrapper.read_file_data(PROGRAM_OPTIONS_FILE)
        if options_text is not None:
            return self._parse_options(options_text)

    def _parse_options(self, options_text):
        lines = options_text.splitlines()
        options = {}
        for line in lines:
            option = self._extract_option(line)
            if option:
                options[option[0]] = option[1]
        return options

    def _extract_option(self, option):
        parts = option.split('=',1)
        if len(parts) == 2:
            return parts

