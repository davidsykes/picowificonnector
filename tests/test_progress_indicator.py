import sys
from machine import Pin, Timer
sys.path.append('../src')
from progress_indicator import ProgressIndicator

class MockPico:
    def __init__(self):
        self.pins = {}
    def set_pin_type(self, name, type):
        self.pins[name] = [type,None]
    def set_pin_value(self, name, value):
        self.pins[name][1] = value
    def get_pin_value(self, name):
        return self.pins[name][1]

class TestProgressIndicator:
    def setup_method(self, test_method):
        Timer.reset()
        self.pico = MockPico()
        Pin.pico = self.pico
        self.progress = ProgressIndicator()
        Pin.led_sequence = [self.pico.pins['LED'][1]]

    def test_the_led_pin_is_made_into_an_output(self):
        assert(self.pico.pins['LED'][0] == Pin.OUT)

    def test_the_progress_indicator_begins_with_the_led_on(self):
        assert(self.pico.pins['LED'][1] == 1)

    def test_the_progress_indiator_sets_up_a_200ms_timer(self):
        assert(Timer.frequency == 5)
        assert(Timer.mode == Timer.PERIODIC)

    def test_progress_0_is_always_on(self):
        self.call_callback(times = 7)
        assert(Pin.led_sequence == [1,1,1,1,1,1,1,1])

    def test_progress_1_flashes_once(self):
        self.progress.set_progress(1)
        self.call_callback(times = 11)
        assert(Pin.led_sequence == [1,0,0,0,1,0,0,0,1,0,0,0])

    def test_progress_2_flashes_twice(self):
        self.progress.set_progress(2)
        self.call_callback(times = 17)
        assert(Pin.led_sequence == [1,0,1,0,0,0,1,0,1,0,0,0,1,0,1,0,0,0])

    def test_progress_5_flashes_5_times(self):
        self.progress.set_progress(5)
        self.call_callback(times = 12)
        assert(Pin.led_sequence == [1,0,1,0,1,0,1,0,1,0,0,0,1])

    def call_callback(self, times):
        for i in range(times):
            Timer.callback(Timer.timer)
            Pin.led_sequence.append(self.pico.pins['LED'][1])