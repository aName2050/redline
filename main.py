from core.wifi_manager import WiFiManager
from core.status_led import StatusLED
from core.rsl import RSL
from core.motor_status import MotorStatusLED
from core.gearbox_motor import GearboxMotor
from core.imu import IMU

import time
import uasyncio as asyncio

# init
led = StatusLED()
wifi = WiFiManager(led)
rsl = RSL(pinR=6, pinG=7, pinB=8)
motorStatus = MotorStatusLED()
imu = IMU()
imu.calibrate()

motorLF = GearboxMotor(14, 15)
motorLR = GearboxMotor(20, 21)
motorRF = GearboxMotor(12, 13)
motorRR = GearboxMotor(10, 11)

motorLF.setInverse(True)
motorRR.setInverse(True)

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

# tasks
async def imu_task():
    while True:
        imu.update()
        await asyncio.sleep_ms(10)

# main loop
# this is where the fun stuff is
async def main():
    asyncio.create_task(imu_task())

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

        await asyncio.sleep_ms(20)

asyncio.run(main())