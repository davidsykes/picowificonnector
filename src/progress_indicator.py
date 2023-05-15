from machine import Pin, Timer

class ProgressIndicator:
	LOOKING_FOR_EXISTING_DETAILS = 1
	CONNECTING = 2
	CONNECTED = 3
	NETWORK_ERROR = 4
	CONNECTING_TIMED_OUT = 5
	INITIALISING_ACCESS_POINT = 6
	ACCESS_POINT_READY = 7

	def __init__(self):
		self.led = Pin("LED", Pin.OUT)
		self.led.value(1)
		self.progress = 0
		self.flash_count = 0
		self.off_count = 0
		self.timer = Timer()
		self.timer.init(freq=5, mode=Timer.PERIODIC, callback=self.blink)

	def blink(self, timer):
		if self.there_is_no_progress_to_report():
			return
		if self.the_led_is_on():
			self.end_a_flash()
			return
		if self.there_are_more_flashes_to_perform():
			self.flash_led()
			return
		if self.are_there_more_off_periods_to_go():
			self.off_count = self.off_count - 1
			return
		self.set_up_new_sequence()
		
	def set_progress(self, progress, message=None):
		self.progress = progress
		self.set_up_new_sequence()

	def there_is_no_progress_to_report(self):
		return self.progress < 1

	def the_led_is_on(self):
		return self.led.value() == 1
	
	def end_a_flash(self):
		self.led.value(0)
		self.flash_count = self.flash_count - 1

	def there_are_more_flashes_to_perform(self):
		return self.flash_count > 0
	
	def flash_led(self):
		self.led.value(1)

	def are_there_more_off_periods_to_go(self):
		return self.off_count > 0
	
	def set_up_new_sequence(self):
		self.led.value(1)
		self.flash_count = self.progress
		self.off_count = 2

	def stop(self):
		self.timer.deinit()