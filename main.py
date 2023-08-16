from network_initialiser import NetworkInitialiser

options = {}
options['ssid'] = 'pico ssid'
options['password'] = '123456789'
options['options'] = [{'name': 'option1', 'text': 'option 1'},{'name': 'option2', 'text': 'option 2'}]

values = NetworkInitialiser().initialise(options)

ip = values['ip']
option1 = values['option1']
option2 = values['option2']

print('ip=',ip)
print('option1=',option1)
print('option2=',option2)