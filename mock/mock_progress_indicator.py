class MockProgressIndicator:
    def set_progress(self, value):
        self.progress = value
        print('Progress:', value)