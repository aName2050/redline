from core import status_led, wifi_manager
import time

# init the stuff
led = status_led.StatusLED()
wifi = wifi_manager.WiFiManager(led)

# boot
led.setState(led.BOOTING)
start = time.ticks_ms() # one day i'll optimize this so its goes lightning fast
while time.ticks_diff(time.ticks_ms(), start) < 4000:
    led.updateLED()

# get the wifi up
if not wifi.start():
    led.setState(led.FAULT)
    while True:
        led.updateLED()
        # ideally you dont want to hang the entire microcontroller
        # this is temp and eventually i'll add proper fault handling
        # but not today :)

# main loop
while True:
    led.updateLED()

    if wifi.hasClient():
        led.setState(led.ENABLED)
    else:
        led.setState(led.WIFI_CONNECTED)
