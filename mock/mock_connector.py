import sys
sys.path.append('../src')
from network_initialiser import NetworkInitialiser
from mock_pico_wrapper import MockPicoWrapper
from mock_progress_indicator import MockProgressIndicator

w = MockPicoWrapper()
p = MockProgressIndicator()
c = NetworkInitialiser(w, p)

c.initialise()