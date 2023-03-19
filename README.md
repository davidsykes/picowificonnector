# picowificonnector

This code is intended to allow a pico to be connected to a wifi network without having to specify the ssid and password in code or a file.

When first run the NetworkInitialiser sets up the pico as an access point with the name PICO and password 12345678.
Logging in and opening a web page generates a form where the ssid and password for the wifi router to connect to can be entered.
The ssid and password is then stored in a file on the pico, and used to connect to the wifi network.

If the connection fails then the access point is set up again allowing a new ssid and password to be entered.

The code allows a progress indicator class to be provided. This class should implement the function set_progress(progress, message)

Progress values:
0   The initial value. The LED is permanently on
1	Look for existing credentials
2	Credentials found, try and connect
3	WiFi connection succeeded
4	Connection failed with negative status code
5	Connection attempt timed out
6	About to set up the access point
7	Access point is active

message is set to the ip address when a connection is made to the wifi router

If no progress indicator is provided then the ProgressIndicator class is used, which flashes the pico led a number of times, according to the current progress value

