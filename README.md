# picowificonnector

This code is intended to allow a pico to be connected to a wifi network without having to program the ssid and password in code

When first run the code sets up the pico as an access point. Logging in and browsing to the pico generates a form where the ssid and password can be entered.
The ssid and password is stored in a file, and used to connect to the wifi network when next run

If the connection fails then the access point is set up again allowing new ssid and password to be entered.

The code allows a progress indicator to be provided. This should implement the function set_progress(int progress)
If no progress indicator is provided then the ProgressIndicator class is used, which flashes the pico led a number of times, according to the current progress value

Progress values:
0   The initial value. The LED is permanently on
1	Look for existing credentials
2	Credentials found, try and connect
3	WiFi connection succeeded
4	Connection failed with negative status code
5	Connection attempt timed out
6	About to set up the access point
7	Access point is active


