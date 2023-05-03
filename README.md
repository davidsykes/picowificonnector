# picowificonnector

This code is intended to allow a pico to be connected to a wifi network without having to specify the ssid and password in code or a file.

When first run the NetworkInitialiser sets up the pico as an access point with the default name PICO and password 12345678.
Logging in and opening a web page generates a form where the ssid and password for the wifi router to connect to can be entered.
The ssid and password is then stored in a file on the pico. When the network initialiser runs again and finds this file it uses it to connect to the wifi network.

If the connection fails then the access point is set up again allowing a new ssid and password to be entered.

The progress of the connection is indicated using the led. At start up the led is on. The led will then flash a number of times to indicate the curremt progress

Progress values:
0   The initial value. The LED is permanently on
1	Look for existing credentials
2	Credentials found, try and connect
3	WiFi connection succeeded
4	Connection failed with negative status code
5	Connection attempt timed out
6	About to set up the access point
7	Access point is active


Using the connector

The simplest way to use the connector is to call initialise()

from network_initialiser import NetworkInitialiser
values = NetworkInitialiser().initialise()

This will create an access point called PICO with password 12345678, and will return a dictionary containing a item 'ip' specifying the current ip

To change the ssid and password of the access point use AccessPointOptions

from network_initialiser import NetworkInitialiser, AccessPointOptions
access_point_options = AccessPointOptions('pico ssd', 'password')
values = NetworkInitialiser().initialise()




The code allows a progress indicator class to be provided. This class should implement the function set_progress(progress, message)


message is set to the ip address when a connection is made to the wifi router

