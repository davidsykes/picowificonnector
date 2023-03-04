class Pin:
    pico = None
    OUT = 1
    def __init__(self, name, type):
        self.name = name
        Pin.pico.set_pin_type(name, type)
    def value(self, v=None):
        if v is not None:
            Pin.pico.set_pin_value(self.name, v)
        return Pin.pico.get_pin_value(self.name)

class Timer:
    PERIODIC = 1
    def init(self, freq, mode, callback):
        Timer.timer = self
        Timer.frequency = freq
        Timer.mode = mode
        Timer.callback = callback
    def reset():
        Timer.timer = None
        Timer.frequency = None
        Timer.mode = None
        Timer.callback = None