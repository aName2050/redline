from core.wifi_manager import WiFiManager
from core.status_led import StatusLED
from core.rsl import RSL
from core.motor_status import MotorStatusLED
from core.gearbox_motor import GearboxMotor
import time
import uasyncio as asyncio

# init
led = StatusLED()
wifi = WiFiManager(led)
rsl = RSL(pinR=6, pinG=7, pinB=8)
motorStatus = MotorStatusLED()

motorLF = GearboxMotor(12, 13)
motorLR = GearboxMotor(14, 15)
motorRF = GearboxMotor(20, 21)
motorRR = GearboxMotor(10, 11)

# drive forward for 5 seconds
motorLF.setSpeed(0.0, motorLF.CONTROL_TYPE['duty_cycle'])
motorLR.setSpeed(0.0, motorLF.CONTROL_TYPE['duty_cycle'])
motorRF.setSpeed(0.0, motorLF.CONTROL_TYPE['duty_cycle'])
motorRR.setSpeed(0.0, motorLF.CONTROL_TYPE['duty_cycle'])

# boot
led.setState(led.BOOTING)
rsl.setState(rsl.OFF)
motorStatus.setDisabled()

start = time.ticks_ms()
while time.ticks_diff(time.ticks_ms(), start) < 6000:
    led.updateLED()

rsl.setState(rsl.DISABLED)

if not wifi.start():
    led.setState(led.FAULT)
    rsl.setState(rsl.ESTOP)
    while True:
        led.updateLED()
        rsl.update()
        # ideally you dont want to hang the entire microcontroller
        # this is temp and eventually i'll add proper fault handling
        # but not today :)

# main loop
# this is where the fun stuff is
async def main():
    while True:
        led.updateLED()
        rsl.update()

        if wifi.hasClient():
            led.setState(led.ENABLED)
            rsl.setState(rsl.ENABLED)
            motorStatus.setEnabled()
            motorStatus.update(motorLF.getSpeed(), motorRF.getSpeed())
        else:
            led.setState(led.WIFI_CONNECTED)
            rsl.setState(rsl.DISABLED)
            motorStatus.setDisabled()

asyncio.run(main())