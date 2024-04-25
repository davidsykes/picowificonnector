from network_initialiser import NetworkInitialiser, AccessPointOptions

access_point_options = AccessPointOptions('pico', '12345678')
values = NetworkInitialiser().initialise(access_point_options)

ip = values['ip']
option1 = values['option1']
option2 = values['option2']

print('ip=',ip)
print('option1=',option1)
print('option2=',option2)