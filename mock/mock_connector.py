import sys
sys.path.append('../src')

from network_initialiser import NetworkInitialiser
from mock_pico_wrapper import MockPicoWrapper

w = MockPicoWrapper()
c = NetworkInitialiser(w)

c.initialise()